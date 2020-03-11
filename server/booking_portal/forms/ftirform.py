from django import forms

from ..models import FTIR
from .userform import UserDetailsForm


class FTIRForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = FTIR
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'composition',
                                                'state',
                                                'solvent',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'composition': 'Composition',
                'state': 'Solid / Liquid',
                'solvent': 'Solvent Used (if any)',
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
                'state': forms.Select(attrs={
                                        'class': 'form-control',
                                    }
                ),
                'solvent': forms.TextInput(attrs={
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