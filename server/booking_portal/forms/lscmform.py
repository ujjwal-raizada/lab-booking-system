from django import forms

from ..models import LSCM
from .userform import UserDetailsForm


class LSCMForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = LSCM
        fields = UserDetailsForm.Meta.fields + ('sample_description',
                                                'dye',
                                                'excitation_wavelength',
                                                'emission_range',
                                                'analysis_details')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_description': 'Sample Description',
                'dye': 'Dye',
                'excitation_wavelength': 'Excitation Wavelength',
                'emission_range': 'Emission Range',
                'analysis_details': 'Analysis Details',
            }
        )
        labels = UserDetailsForm.Meta.labels
        UserDetailsForm.Meta.widgets.update(
            {
                'sample_description': forms.TextInput(attrs={
                                                        'class': 'form-control',
                                                      }
                ),
                'dye': forms.TextInput(attrs={
                                         'class': 'form-control',
                                       }
                ),
                'excitation_wavelength': forms.TextInput(attrs={
                                                           'class': 'form-control',
                                                         }
                ),
                'emission_range': forms.TextInput(attrs={
                                                    'class': 'form-control',
                                                  }
                ),
                'analysis_details': forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                    }
                ),
            }
        )