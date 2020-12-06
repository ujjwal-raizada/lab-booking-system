from django import forms

from ..models.instrument.form_models import HPLC
from .userform import UserDetailsForm


class HPLCForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = HPLC
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'sample_information',
                                                'mobile_phase',
                                                'column_for_lc',
                                                'detection_wavelength',
                                                'other_information')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'sample_information': 'Sample information / composition',
                'mobile_phase': 'Mobile Phase Composition',
                'column_for_lc': 'Column for LC',
                'detection_wavelength': 'Detection Wavelength(s)',
                'other_information': 'Any other information',
            }
        )
        labels = UserDetailsForm.Meta.labels
        UserDetailsForm.Meta.widgets.update(
            {
                'sample_code': forms.TextInput(attrs={
                                                 'class': 'form-control',
                                               }
                ),
                'sample_information': forms.TextInput(attrs={
                                                        'class': 'form-control',
                                                      }
                ),
                'mobile_phase': forms.TextInput(attrs={
                                                  'class': 'form-control',
                                                }
                ),
                'column_for_lc': forms.TextInput(attrs={
                                                   'class': 'form-control',
                                                 }
                ),
                'detection_wavelength': forms.TextInput(attrs={
                                                          'class': 'form-control',
                                                        }
                ),
                'other_information': forms.Textarea(attrs={
                                                      'class': 'form-control',
                                                    }
                ),
            }
        )
        widgets = UserDetailsForm.Meta.widgets