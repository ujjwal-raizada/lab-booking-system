from django import forms

from ..models.instrument.form_models import LCMS
from .userform import UserDetailsForm


class LCMSForm(UserDetailsForm):
  class Meta(UserDetailsForm.Meta):
      model = LCMS
      fields = UserDetailsForm.Meta.fields + ('sample_code',
                                              'composition',
                                              'phase',
                                              'no_of_lc_peaks',
                                              'solvent_solubility',
                                              'exact_mass',
                                              'mass_adducts',
                                              'analysis_mode',
                                              'other_remarks')
      UserDetailsForm.Meta.labels.update(
          {
              'sample_code': 'Sample Code',
              'composition': 'Sample Information / Composition',
              'phase': 'Mobile Phase and Column for LC',
              'no_of_lc_peaks': 'No. of LC peaks',
              'solvent_solubility': 'Solvent Solubility',
              'exact_mass': 'Exact Mass',
              'mass_adducts': 'Expected Mass Adducts',
              'analysis_mode': 'Mode of Analysis (Positive / Negative)',
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
              'composition': forms.TextInput(attrs={
                                              'class': 'form-control',
                                            }
              ),
              'phase': forms.TextInput(attrs={
                                          'class': 'form-control',
                                      }
              ),
              'no_of_lc_peaks': forms.NumberInput(attrs={
                                                    'class':' form-control',
                                                  }
              ),
              'solvent_solubility': forms.TextInput(attrs={
                                                      'class': 'form-control',
                                                    }
              ),
              'exact_mass': forms.TextInput(attrs={
                                              'class': 'form-control',
                                            }
              ),
              'mass_adducts': forms.TextInput(attrs={
                                                'class': 'form-control',
                                              }
              ),
              'analysis_mode': forms.Select(attrs={
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