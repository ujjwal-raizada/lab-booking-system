from django import forms
from booking_portal.models import Instrument, Slot


class IntrumentList(forms.Form):
    instruments = forms.ModelChoiceField(queryset=Instrument.objects.all())

class SlotList(forms.Form):
    def __init__(self, instr_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slots'] = forms.ModelChoiceField(
            queryset=Slot.objects.filter(instrument=instr_id,
                                         status=Slot.STATUS_1))
