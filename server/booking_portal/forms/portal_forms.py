from django import forms
from booking_portal.models import Instrument


class IntrumentList(forms.Form):
    instruments = forms.ModelChoiceField(queryset=Instrument.objects.all())
