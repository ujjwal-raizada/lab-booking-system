from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email

from .user import CustomUserAdmin
from ... import forms
from ...models import Student, Faculty


class StudentAdmin(CustomUserAdmin):
    CSV_HEADERS_STUDENT = ('supervisor',)

    form = forms.StudentChangeForm
    add_form = forms.StudentCreationForm

    list_filter = CustomUserAdmin.list_filter + ('supervisor', )
    list_display = CustomUserAdmin.list_display + ('supervisor',)
    fieldsets = CustomUserAdmin.fieldsets + (
        (None, {'fields': ('supervisor',)},),
    )
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('supervisor',)}
        ),
    )

    def _validate_record(self, record):
        record = super()._validate_record(record)

        record['supervisor'] = record['supervisor'].strip()
        validate_email(record['supervisor'])

        obj = Faculty.objects.filter(email=record['supervisor']).first()
        if not obj:
            raise ObjectDoesNotExist(f"Supervisor doesn't exist: \"{record['supervisor']}\"")

        record['supervisor'] = obj
        return record

    def get_user_type(self, request):
        return Student

    def is_user_staff(self):
        return False

    def get_csv_headers(self):
        return super().get_csv_headers() + self.CSV_HEADERS_STUDENT
