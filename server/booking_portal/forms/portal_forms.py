from django import forms
import datetime

from ..models.instrument import Instrument
from ..models.slot import Slot


class SlotModelChoiceField(forms.ModelChoiceField):
    """Provides customized representation for
    Slot Field in ModelChoiceField"""

    def label_from_instance(self, obj):
        # Returns description property of Slot Model
        return obj.description


class IntrumentList(forms.Form):
    instruments = forms.ModelChoiceField(queryset=Instrument.objects.all())


class SlotList(forms.Form):
    def __init__(self, instr_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slots'] = SlotModelChoiceField(
            queryset=Slot.objects.filter(instrument=instr_id,
                                         status=Slot.STATUS_1,
                                         date__gte=datetime.date.today()))
