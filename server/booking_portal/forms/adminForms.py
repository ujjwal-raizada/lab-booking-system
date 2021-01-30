import datetime

from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from ..models.instrument import Instrument
from ..models.user import CustomUser, Student, Faculty, LabAssistant


EMAIL_CHOICES = (
    ("Yes", "Yes"),
    ("No", "No"),
)

BOOL_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)

START_TIME_CHOICES = (
    ('00:00:00', '12 AM (Midnight)'),
    ('01:00:00', '01 AM'),
    ('02:00:00', '02 AM'),
    ('03:00:00', '03 AM'),
    ('04:00:00', '04 AM'),
    ('05:00:00', '05 AM'),
    ('06:00:00', '06 AM'),
    ('07:00:00', '07 AM'),
    ('08:00:00', '08 AM'),
    ('09:00:00', '09 AM'),
    ('10:00:00', '10 AM'),
    ('11:00:00', '11 AM'),
    ('12:00:00', '12 PM (Noon)'),
    ('13:00:00', '01 PM'),
    ('14:00:00', '02 PM'),
    ('15:00:00', '03 PM'),
    ('16:00:00', '04 PM'),
    ('17:00:00', '05 PM'),
    ('18:00:00', '06 PM'),
    ('19:00:00', '07 PM'),
    ('20:00:00', '08 PM'),
    ('21:00:00', '09 PM'),
    ('22:00:00', '10 PM'),
    ('23:00:00', '11 PM'),
)

DURATION = (
    ('1-hour', '1-hour'),
    ('2-hour', '2-hour'),
    ('3-hour', '3-hour'),
    ('4-hour', '4-hour'),
    ('6-hour', '6-hour'),
    ('8-hour', '8-hour'),
)

DELTA_DAYS = (
    ('1', '1-day (Selected Date only)'),
    ('7', '1-week'),
    ('14', '2-weeks'),
    ('30', '1-month'),
    ('60', '2-month'),
)


class BulkImportForm(forms.Form):
    """Form for importing users from CSV"""

    csv_file = forms.FileField()
    send_email = forms.ChoiceField(
        choices=EMAIL_CHOICES, initial=EMAIL_CHOICES[1])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_val in self.Meta.fields:
            self.fields[field_val].label = self.Meta.labels.get(field_val)

    class Meta:
        fields = ('csv_file', 'send_email')
        labels = {
            'csv_file': 'Upload CSV File',
            'send_email': 'Do you want to send password details to users?',
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class BulkTimeSlotForm(forms.Form):
    """Form for bulk time slot creation"""

    instruments = forms.ModelChoiceField(
        queryset=Instrument.objects.all(),
        label="Select Instrument",
    )
    start_date = forms.DateField(
        initial=datetime.date.today,
        widget=DateInput,
        label="Date from/on which the slot has to be made",
    )
    for_the_next = forms.ChoiceField(
        choices=DELTA_DAYS,
        label="For how many days do you want to add the slots?",
    )
    start_time = forms.ChoiceField(
        choices=START_TIME_CHOICES,
        initial=START_TIME_CHOICES[8],
        label="Start Time",
    )
    end_time = forms.ChoiceField(
        choices=START_TIME_CHOICES,
        initial=START_TIME_CHOICES[9],
        label="End Time",
    )
    lab_duration = forms.ChoiceField(
        choices=DURATION,
        label="Slot Duration",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')


class StudentCreationForm(CustomUserCreationForm):
    class Meta:
        model = Student
        fields = ('supervisor',)


class StudentChangeForm(CustomUserChangeForm):
    class Meta:
        model = Student
        fields = ('supervisor',)


class FacultyCreationForm(CustomUserCreationForm):
    class Meta:
        model = Faculty
        fields = ('department',)


class FacultyChangeForm(CustomUserChangeForm):
    class Meta:
        model = Faculty
        fields = ('department',)


class InstrumentCreateForm(forms.ModelForm):

    class Meta:
        model = Instrument
        fields = ('name', 'desc', 'status')
        widgets = {
            'status': forms.Select(
                choices=BOOL_CHOICES
            ),
        }


class InstrumentChangeForm(forms.ModelForm):

    class Meta:
        model = Instrument
        fields = ('name', 'desc', 'status',)
        widgets = {
            'status' : forms.Select(
                choices=BOOL_CHOICES
            ),
        }