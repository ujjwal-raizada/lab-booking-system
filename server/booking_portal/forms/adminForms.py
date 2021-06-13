import datetime

from crispy_forms.bootstrap import PrependedAppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, ButtonHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from ..models.instrument import Instrument
from ..models.slot import SlotManager
from ..models.user import CustomUser, Student, Faculty

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


class CrispyTimeField(Field):
    def __init__(self, *args, **kwargs):
        kwargs['template'] = 'widgets/time_input.html'
        kwargs['css_class'] = 'datetimepicker-input'
        super().__init__(*args, **kwargs)


class MinuteDurationField(forms.DurationField):
    default_error_messages = {
        'invalid': 'The duration in minutes must be a positive integer.'
    }

    def to_python(self, value):
        validation_error = ValidationError(self.error_messages['invalid'])
        if isinstance(value, datetime.timedelta):
            return value

        try:
            value = int(value)
        except (ValueError, TypeError):
            raise validation_error
        else:
            if value > 0:
                return datetime.timedelta(minutes=int(value))
            raise validation_error


class BulkCreateSlotsForm(forms.Form):
    """Form for bulk time slot creation"""

    instrument = forms.ModelChoiceField(
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
    start_time = forms.TimeField(
        label="Start Time",
    )
    end_time = forms.TimeField(
        label="End Time",
    )
    slot_duration = MinuteDurationField(
        label="Slot Duration",
        help_text="The duration of each slot specified in minutes. If a whole number"
                  " of slots cannot be created between the start and end time, no"
                  " slots will be created.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-3'
        self.helper.layout = Layout(
            'instrument',
            'start_date',
            'for_the_next',
            CrispyTimeField('start_time'),
            CrispyTimeField('end_time'),
            PrependedAppendedText(
                'slot_duration',
                appended_text='minutes'
            ),
            ButtonHolder(
                Submit('add_slots', value="Add Slots")
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date: datetime.date = cleaned_data.get('start_date')
        start_time: datetime.time = cleaned_data.get('start_time')
        end_time: datetime.time = cleaned_data.get('end_time')
        duration: datetime.timedelta = cleaned_data.get('slot_duration')
        day_count = int(cleaned_data.get('for_the_next'))

        if start_time >= end_time:
            self.add_error(
                'start_time',
                ValidationError("Start time cannot be after end time.")
            )

        if start_date < datetime.date.today():
            self.add_error(
                "start_date",
                ValidationError("Start date cannot be before today.")
            )

        combined_start_time = datetime.datetime.combine(start_date, start_time)
        combined_end_time = datetime.datetime.combine(start_date, end_time)
        if duration and not float.is_integer((combined_end_time - combined_start_time) / duration):
            self.add_error(
                None,
                ValidationError("Cannot create whole number of slots between "
                                "specified start and end time with the given duration.")
            )

        next_days = SlotManager.get_valid_slot_days(start_date, day_count)
        if not next_days:
            self.add_error(
                None,
                ValidationError("No days available to create slots! Note that "
                                "slots cannot be created on Sundays.")
            )

        return cleaned_data


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