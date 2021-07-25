from django import forms
from django.utils.timezone import now

from ..models.instrument import Instrument
from ..models.slot import Slot


class SlotModelChoiceField(forms.ModelChoiceField):
    """Provides customized representation for
    Slot Field in ModelChoiceField"""

    def label_from_instance(self, obj):
        # Returns description property of Slot Model
        return obj.description


class InstrumentList(forms.Form):
    """Form for selecting instruments for booking"""
    instruments = forms.ModelChoiceField(queryset=Instrument.objects.all())


class SlotList(forms.Form):
    """Form for selecting an empty slot of a given
    instrument"""
    def __init__(self, instr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slots'] = SlotModelChoiceField(
            queryset=Slot.objects.filter(
                instrument=instr,
                status=Slot.STATUS_1,
                date__gte=now().date()
            )
)
