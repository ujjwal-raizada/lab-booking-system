from django import forms

from ..models.instrument.form_models import Rheometer
from .userform import UserDetailsForm


class RheometerForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = Rheometer
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'ingredient_details',
                                                'physical_characteristics',
                                                'chemical_nature',
                                                'origin',
                                                'analysis_required',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'ingredient_details': 'Details of ingredients (Solute + Solvent or Solute + Solvent + additives etc.)',
                'physical_characteristics': 'Details of Pyhsical Characteristics [Concentration, gel/crystallization temperature and approx viscosity (mPa.s)]',
                'chemical_nature': 'Chemical Nature of Sample (Acidic / Basic / Neutral / pH range etc.)',
                'origin': 'Origin (natural or synthetic)',
                'analysis_required': 'Analysis required [Viscosity, Modulus]',
                'other_remarks': 'Any other relevant information'
            }
        )
        labels = UserDetailsForm.Meta.labels
        UserDetailsForm.Meta.widgets.update(
            {
                'sample_code': forms.TextInput(attrs={
                                                 'class': 'form-control',
                                              }
                ),
                'ingredient_details': forms.TextInput(attrs={
                                                         'class': 'form-control',
                                                       }
                ),
                'physical_characteristics': forms.TextInput(attrs={
                                                              'class': 'form-control',
                                                            }
                ),
                'chemical_nature': forms.TextInput(attrs={
                                                     'class': 'form-control',
                                                   }
                ),
                'origin': forms.Select(attrs={
                                         'class': 'form-control',
                                       }
                ),
                'analysis_required': forms.TextInput(attrs={
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