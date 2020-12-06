from django import forms

from ..models.instrument.form_models import SCXRD
from .userform import UserDetailsForm


class SCXRDForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = SCXRD
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'chemical_composition',
                                                'scanning_rate',
                                                'source',
                                                'any_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'chemical_composition': 'Chemical Composition',
                'scanning_rate': 'Scanning Rate',
                'source': 'X-ray source to be used (Cu or Mo)',
                'any_remarks': 'Any other remarks',
            }
        )
        labels = UserDetailsForm.Meta.labels
        UserDetailsForm.Meta.widgets.update(
            {
                'sample_code': forms.TextInput(attrs={
                                                 'class': 'form-control',
                                               }
                ),
                'chemical_composition': forms.TextInput(attrs={
                                                          'class': 'form-control',
                                                        }
                ),
                'scanning_rate': forms.TextInput(attrs={
                                                   'class': 'form-control',
                                                 }
                ),
                'source': forms.Select(attrs={
                                         'class': 'form-control',
                                       }
                ),
                'any_remarks': forms.Textarea(attrs={
                                                'class': 'form-control',
                                              }
                ),
            }
        )
        widgets = UserDetailsForm.Meta.widgets