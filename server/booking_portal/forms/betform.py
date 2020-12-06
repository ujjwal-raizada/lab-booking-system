from django import forms

from ..models.instrument.form_models import BET
from .userform import UserDetailsForm


class BETForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = BET
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'pretreatment_conditions',
                                                'precautions',
                                                'adsorption',
                                                'surface_area',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'pretreatment_conditions': 'Pretreatment Conditions',
                'precautions': 'Precautions to be taken',
                'adsorption': 'N2 / CO2 Adsorption',
                'surface_area': 'Specific surface area / surface area and pore size analysis to be required',
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
                'pretreatment_conditions': forms.TextInput(attrs={
                                                             'class': 'form-control',
                                                           }
                ),
                'precautions': forms.TextInput(attrs={
                                                 'class': 'form-control',
                                               }
                ),
                'adsorption': forms.TextInput(attrs={
                                                'class': 'form-control',
                                              }
                ),
                'surface_area': forms.TextInput(attrs={
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