import csv
from io import TextIOWrapper

from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.contrib import admin, messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from .models import CustomUser, Student, Faculty, EmailModel, LabAssistant
from .models import Instrument, Slot, Request
from .models import FTIR, FESEM, LCMS, TCSPC, UserDetails
from .forms.adminForms import BulkImportForm


CSV_HEADERS = ('username', 'password')

def create_users(user_type, records):
    headers = CSV_HEADERS
    if set(records.fieldnames) != set(headers):
        raise Exception(f"Invalid CSV headers/columns. Expected: {headers}")
    for record in records:
        record['password'] = make_password(record['password'])
        user_type.objects.create(**record)


class BulkImportAdmin(UserAdmin):
    change_list_template = "admin/csv_change_list.html"

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
                    user_type = Student
                elif '/faculty/' in request.path:
                    user_type = Faculty
                elif '/labassistant/' in request.path:
                    user_type = LabAssistant
                else:
                    raise Http404
                create_users(user_type, reader)
            except Exception as err:
                messages.error(request, f'Error on row number {reader.line_num}: {err}')
            else:
                messages.success(request, "Your csv file has been imported")
            return redirect("..")
        form = BulkImportForm()
        payload = {"form": form}
        return render(
            request, "admin/bulk_import_form.html", payload
        )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student, BulkImportAdmin)
admin.site.register(Faculty, BulkImportAdmin)
admin.site.register(EmailModel)
admin.site.register(LabAssistant, BulkImportAdmin)
admin.site.register(Instrument)
admin.site.register(Slot)
admin.site.register(Request)
admin.site.register(FTIR)
admin.site.register(FESEM)
admin.site.register(LCMS)
admin.site.register(TCSPC)
admin.site.register(UserDetails)