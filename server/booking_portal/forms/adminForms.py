from django import forms
from django.contrib.admin import widgets
from ..models import Instrument
import datetime

class BulkImportForm(forms.Form):
    csv_file = forms.FileField()

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
    ('4-hour', '4-hour'),
    ('3-hour', '3-hour'),
)

DELTA_DAYS = (
    ('1', '1-day'),
    ('7', '1-week'),
    ('14', '2-weeks'),
    ('30', '1-month'),
    ('60', '2-month'),
)

class DateInput(forms.DateInput):
    input_type = 'date'

class BulkTimeSlotForm(forms.Form):
    instruments = forms.ModelChoiceField(queryset=Instrument.objects.all())
    date = forms.DateField(initial=datetime.date.today, widget=DateInput)
    for_the_next = forms.ChoiceField(choices=DELTA_DAYS)
    start_time = forms.ChoiceField(choices=START_TIME_CHOICES)
    end_time = forms.ChoiceField(choices=START_TIME_CHOICES)
    lab_duration = forms.ChoiceField(choices=DURATION)
