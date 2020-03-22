from django import forms

from ..models import DSC
from .userform import UserDetailsForm


class DSCForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = DSC
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'chemical_composition',
                                                'sample_amount',
                                                'heating_program',
                                                'temp_range',
                                                'atmosphere',
                                                'heating_rate',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'chemical_composition': 'Chemical Composition',
                'sample_amount': 'Amount of Sample / mg',
                'heating_program': 'Heating Program (dynamic / isothermal)',
                'temp_range': 'Temperature Range (in degree celsius)',
                'atmosphere': 'Atmosphere (N2, Ar, Air)',
                'heating_rate': 'Heating Rate / C min^-1',
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
                'chemical_composition': forms.TextInput(attrs={
                                                          'class': 'form-control',
                                                        }
                ),
                'sample_amount': forms.TextInput(attrs={
                                                   'class': 'form-control',
                                                 }
                ),
                'heating_program': forms.Select(attrs={
                                                  'class': 'form-control',
                                                }
                ),
                'temp_range': forms.TextInput(attrs={
                                                'class': 'form-control',
                                              }
                ),
                'atmosphere': forms.Select(attrs={
                                             'class': 'form-control',
                                           }
                ),
                'heating_rate': forms.TextInput(attrs={
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