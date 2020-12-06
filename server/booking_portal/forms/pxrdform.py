from django import forms

from ..models.instrument.form_models import PXRD
from .userform import UserDetailsForm


class PXRDForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = PXRD
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'chemical_composition',
                                                'sample_description',
                                                'range',
                                                'scanning_rate',
                                                'any_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'chemical_composition': 'Chemical Composition',
                'sample_description': 'Sample Description (Film/ Powder/ Pellet)',
                'range': '2-theta Range',
                'scanning_range': 'Scanning Rate (degree/min)',
                'any_remarks': 'Any remarks',
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
                'sample_description': forms.Select(attrs={
                                                     'class': 'form-control',
                                                    }
                ),
                'range': forms.TextInput(attrs={
                                           'class': 'form-control',
                                         }
                ),
                'scanning_rate': forms.TextInput(attrs={
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