import csv
import datetime
from io import TextIOWrapper

from django.urls import path
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin

from ... import models
from ... import forms

CSV_HEADERS = ('name', 'email', 'password')
CSV_HEADERS_STUDENT = CSV_HEADERS + ('supervisor',)
CSV_HEADERS_FACULTY = CSV_HEADERS + ('department', )

class CustomUserAdmin(UserAdmin):
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm

    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
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

    def create_users(self, user_type, records):
        headers = CSV_HEADERS
        if user_type == models.Student:
            headers = CSV_HEADERS_STUDENT
        elif user_type == models.Faculty:
            headers = CSV_HEADERS_FACULTY

        if set(records.fieldnames) != set(headers):
            raise Exception(f"Invalid CSV headers/columns. Expected: {headers}")

        for record in records:
            record['password'] = make_password(record['password'])
            if user_type == models.Student:
                obj = models.Faculty.objects.filter(email=record['supervisor']).first()
                if not obj:
                    raise Exception(f"Invalid Supervisor Name: \"{record['supervisor']}\"")
                else:
                    record['supervisor'] = obj

            if user_type.objects.filter(email=record['email']).exists():
                raise Exception(f"User with username \"{record['email']}\" already exists.")
            else:
                user_type.objects.create(**record)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            try:
                csv_file = TextIOWrapper(
                    request.FILES['csv_file'].file,
                    encoding=request.encoding
                )
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                csv_file.seek(0)
                reader = csv.DictReader(csv_file, dialect=dialect)
            except Exception as err:
                self.message_user(request, "Error: {}".format(err))
                return redirect("..")
            try:
                if '/student/' in request.path:
                    user_type = models.Student
                elif '/faculty/' in request.path:
                    user_type = models.Faculty
                elif '/labassistant/' in request.path:
                    user_type = models.LabAssistant
                else:
                    raise Http404
                self.create_users(user_type, reader)
            except Exception as err:
                messages.error(request, f'Error on row number {reader.line_num}: {err}')
            else:
                messages.success(request, "Your csv file has been imported")
            return redirect("..")
        form = forms.BulkImportForm()
        payload = {"form": form}
        return render(
            request, "admin/bulk_import_form.html", payload
        )