from django import forms

from ..models.instrument.form_models import NMR
from .userform import UserDetailsForm


class NMRForm(UserDetailsForm):
    class Meta(UserDetailsForm):
        model = NMR
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'sample_nature',
                                                'quantity',
                                                'solvent',
                                                'analysis',
                                                'experiment',
                                                'spectral_range',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'sample_nature': 'Nature of Sample (Solid or Liquid)',
                'quantity': 'Quantity (in mg)',
                'solvent': 'Solvent for NMR',
                'analysis': 'NMR Analysis (Nuclei)',
                'experiment': '2D-NMR Experiment (if any)',
                'spectral_range': 'Plotting spectral range in ppm (if any)',
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
                'quantity': forms.TextInput(attrs={
                                              'class': 'form-control',
                                            }
                ),
                'solvent': forms.TextInput(attrs={
                                             'class': 'form-control',
                                           }
                ),
                'analysis': forms.TextInput(attrs={
                                              'class': 'form-control',
                                            }
                ),
                'experiment': forms.TextInput(attrs={
                                                'class': 'form-control',
                                              }
                ),
                'spectral_range': forms.TextInput(attrs={
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