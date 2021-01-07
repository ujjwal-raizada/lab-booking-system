import csv
import datetime
from io import TextIOWrapper

from django.urls import path
from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from ... import models
from ... import forms
from ... import permissions

# Allowed headers for different CSV files
CSV_HEADERS = ('name', 'email', 'password')
CSV_HEADERS_STUDENT = CSV_HEADERS + ('supervisor',)
CSV_HEADERS_FACULTY = CSV_HEADERS + ('department', )


class CustomUserAdmin(UserAdmin):
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm

    list_display = ('name', 'email')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)

    change_list_template = "admin/csv_change_list.html"

    def create_users(self, user_type, records, staff=False, notify_user=False):
        """
        Function to create users in bulk from a set of records
        """
        headers = CSV_HEADERS
        if user_type == models.Student:
            headers = CSV_HEADERS_STUDENT
        elif user_type == models.Faculty:
            headers = CSV_HEADERS_FACULTY

        if set(records.fieldnames) != set(headers):
            raise Exception(
                f"Invalid CSV headers/columns. Expected: {headers}")

        for record in records:
            pswd_text = record['password']
            record['password'] = make_password(record['password'])
            if user_type == models.Student:
                obj = models.Faculty.objects.filter(
                    email=record['supervisor']).first()
                if not obj:
                    raise Exception(
                        f"Invalid Supervisor Name: \"{record['supervisor']}\"")
                else:
                    record['supervisor'] = obj

            if user_type.objects.filter(email=record['email']).exists():
                raise Exception(
                    f"User with username \"{record['email']}\" already exists.")
            else:
                user = user_type.objects.create(**record)
                if (staff):
                    user.is_staff = True
                    user.save()

            if notify_user:
                text = render_to_string('email/welcome.html', {
                    'receipent_name': user.name,
                    'email': user.email,
                    'password': pswd_text,
                    'user_type': permissions.get_user_type(user),
                })

                send_mail(
                    subject="Welcome to OnlineCAL !",
                    message=strip_tags(text),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email, ],
                    fail_silently=settings.DEBUG,
                    html_message=text,
                )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """
        Function to bulk import user details from a CSV file
        """

        if request.method == "POST":
            try:
                csv_file = TextIOWrapper(
                    request.FILES['csv_file'].file,
                    encoding=request.encoding
                )
                dialect = csv.Sniffer().sniff(csv_file.read())
                csv_file.seek(0)
                reader = csv.DictReader(csv_file, dialect=dialect)
            except Exception as err:
                self.message_user(request, "Error: {}".format(err))
                return redirect("..")
            try:

                # This flag sets "is_staff" boolean
                staff = False
                if '/student/' in request.path:
                    user_type = models.Student
                elif '/faculty/' in request.path:
                    user_type = models.Faculty
                elif '/labassistant/' in request.path:
                    user_type = models.LabAssistant
                    staff = True
                else:
                    raise Http404

                # If send_email is true, then the new user will receive email
                send_email = False if request.POST.get(
                    'send_email') == "No" else True

                self.create_users(user_type, reader, staff, send_email)

            except Exception as err:
                messages.error(
                    request, f'Error on row number {reader.line_num}: {err}')
            else:
                messages.success(request, "Your csv file has been imported")
            return redirect("..")

        else:
            form = forms.BulkImportForm()
            payload = {"form": form}
            return render(
                request, "admin/bulk_import_form.html", payload
            )
