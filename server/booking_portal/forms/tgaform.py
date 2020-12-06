from django import forms

from ..models.instrument.form_models import TGA
from .userform import UserDetailsForm


class TGAForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = TGA
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'chemical_composition',
                                                'sample_amount',
                                                'heating_program',
                                                'temperature',
                                                'atmosphere',
                                                'heating_rate',
                                                'sample_solubility',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'chemical_composition': 'Chemical Composition',
                'sample_amount': 'Amount of Sample / mg',
                'heating_program': 'Heating program (dynamic / isothermal)',
                'temperature': 'Temperature Range in Celsius',
                'atmosphere': 'Atmosphere (N2, Ar, Air)',
                'heating_rate': 'Heating Rate / C min-1',
                'sample_solubility': 'Solubility of the sample',
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
                'temperature': forms.TextInput(attrs={
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
                'sample_solubility': forms.TextInput(attrs={
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