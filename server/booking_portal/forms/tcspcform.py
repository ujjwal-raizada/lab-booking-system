from django import forms

from ..models.instrument.form_models import TCSPC
from .userform import UserDetailsForm


class TCSPCForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = TCSPC
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'sample_nature',
                                                'chemical_composition',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'sample_nature': 'Nature of Sample',
                'chemical_composition': 'Chemical Composition',
                'other_remarks': 'Any other relevant information',
            }
        )
        labels = UserDetailsForm.Meta.labels
        UserDetailsForm.Meta.widgets.update(
            {
                'sample_code': forms.TextInput(attrs={
                                                'class': 'form-control',
                                            }
                ),
                'sample_nature': forms.Select(attrs={
                                                'class': 'form-control',
                                            }
                ),
                'chemical_composition': forms.TextInput(attrs={
                                                        'class': 'form-control',
                                                        }
                ),
                'other_remarks': forms.Textarea(attrs={
                                                'class': 'form-control',
                                                }
                ),
            }
        )
        widgets = UserDetailsForm.Meta.widgets