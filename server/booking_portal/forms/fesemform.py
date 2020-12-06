from django import forms

from ..models.instrument.form_models import FESEM
from .userform import UserDetailsForm


class FESEMForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = FESEM
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'sample_nature',
                                                'analysis_nature',
                                                'sputter_required',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'sample_nature': 'Nature of Sample',
                'analysis_nature': 'Nature of Analysis (SEM, EDX, STEM etc.)',
                'sputter_required': 'Sputter coating required',
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
                'analysis_nature': forms.TextInput(attrs={
                                                        'class': 'form-control',
                                                    }
                ),
                'sputter_required': forms.Select(attrs={
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