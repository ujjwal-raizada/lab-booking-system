from django import forms

from ..models import UVSpectrophotometer
from .userform import UserDetailsForm


class UVSpectrophotometerForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = UVSpectrophotometer
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'sample_composition',
                                                'molecular_weight',
                                                'analysis_mode',
                                                'wavelength',
                                                'ordinate_mode',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'sample_composition': 'Sample Composition',
                'molucular_weight': 'Molecular weight of the sample (if mode of analysis is liquid)',
                'analysis_mode': 'Mode of analysis',
                'wavelength': 'Wavelength range for analysis',
                'ordinate_mode': 'Ordinate Mode %A%T%R',
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
                'sample_composition': forms.TextInput(attrs={
                                                        'class': 'form-control',
                                                      }
                ),
                'molecular_weight': forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                    }
                ),
                'analysis_mode': forms.Select(attrs={
                                                'class': 'form-control',
                                              }
                ),
                'wavelength': forms.TextInput(attrs={
                                                'class': 'form-control',
                                              }
                ),
                'ordinate_mode': forms.TextInput(attrs={
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