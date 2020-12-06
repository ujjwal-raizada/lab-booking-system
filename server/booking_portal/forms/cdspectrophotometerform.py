from django import forms

from ..models.instrument.form_models import CDSpectrophotometer
from .userform import UserDetailsForm


class CDSpectrophotometerForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = CDSpectrophotometer
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'wavelength_scan_start',
                                                'wavelength_scan_end',
                                                'wavelength_fixed',
                                                'temp_range_scan_start',
                                                'temp_range_scan_end',
                                                'temp_range_fixed',
                                                'concentration',
                                                'cell_path_length',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'wavelength_scan_start': 'Wavalength Range - Scan - Start',
                'wavelength_scan_end': 'Wavelength Range - Scan - End',
                'wavelength_fixed': 'Wavelength Range - Fixed',
                'temp_range_scan_start': 'Temperature Range (20-70 C) - Scan - Start',
                'temp_range_scan_end': 'Temperature Range (20-70 C) - Scan - End',
                'temp_range_fixed': 'Temperature Range (20-70 C) - Fixed',
                'concentration': 'Concentration in mg/ml',
                'cell_path_length': 'Cell path length 0.1 / 0.2 / 0.5 / 1 cm',
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
                'wavelength_scan_start': forms.TextInput(attrs={
                                                           'class': 'form-control',
                                                         }
                ),
                'wavelength_scan_end': forms.TextInput(attrs={
                                                         'class': 'form-control',
                                                       }
                ),
                'wavelength_fixed': forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                    }
                ),
                'temp_range_scan_start': forms.TextInput(attrs={
                                                           'class': 'form-control',
                                                         }
                ),
                'temp_range_scan_end': forms.TextInput(attrs={
                                                         'class': 'form-control',
                                                       }
                ),
                'temp_range_fixed': forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                    }
                ),
                'concentration': forms.TextInput(attrs={
                                                   'class': 'form-control',
                                                 }
                ),
                'cell_path_length': forms.TextInput(attrs={
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