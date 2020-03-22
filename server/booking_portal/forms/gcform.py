from django import forms

from ..models import GC
from .userform import UserDetailsForm


class GCForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = GC
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'appearance',
                                                'no_of_gc_peaks',
                                                'solvent_solubility',
                                                'column_details',
                                                'exp_mol_wt',
                                                'mp_bp',
                                                'sample_source',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'appearance': 'Color and Appearance',
                'no_of_gc_peaks': 'No. of GC Peaks',
                'solvent_solubility': 'Solvent Solubility',
                'column_details': 'Column Details',
                'exp_mol_wt': 'Exp. Mol. Wt.',
                'mp_bp': 'MP / BP (C)',
                'sample_source': 'Sample Source (Natural/ Synthesis/ Waste)',
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
                'appearance': forms.TextInput(attrs={
                                                'class': 'form-control',
                                              }
                ),
                'no_of_gc_peaks': forms.NumberInput(attrs={
                                                      'class': 'form-control',
                                                    }
                ),
                'solvent_solubility': forms.TextInput(attrs={
                                                        'class': 'form-control',
                                                      }
                ),
                'column_details': forms.TextInput(attrs={
                                                    'class': 'form-control',
                                                  }
                ),
                'exp_mol_wt': forms.TextInput(attrs={
                                                'class': 'form-control',
                                              }
                ),
                'mp_bp': forms.TextInput(attrs={
                                           'class': 'form-control',
                                         }
                ),
                'sample_source': forms.Select(attrs={
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