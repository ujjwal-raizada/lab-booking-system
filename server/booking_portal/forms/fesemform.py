from django import forms

from ..models.instrument.form_models import FESEM
from .userform import UserDetailsForm, UserRemarkForm


class FESEMForm (UserDetailsForm, UserRemarkForm):
    title = "Field Emission Scanning Electron Microscope"
    subtitle = "Field Emission Scanning Electron Microscope"
    help_text = '''
    '''
    class Meta(UserDetailsForm.Meta, UserRemarkForm.Meta):
        model = FESEM
        fields = UserDetailsForm.Meta.fields + \
            (
                'sample_code',
                'sample_nature',
                'analysis_nature',
                'sputter_required',
            ) + \
            UserRemarkForm.Meta.fields

        labels = dict(
            ** UserDetailsForm.Meta.labels,
            ** UserRemarkForm.Meta.labels,
            ** {
                'sample_code': 'Sample Code',
                'sample_nature': 'Nature of Sample',
                'analysis_nature': 'Nature of Analysis (SEM, EDX, STEM etc.)',
                'sputter_required': 'Sputter coating required',
            },
        )

        widgets = dict(
            ** UserDetailsForm.Meta.widgets,
            ** UserRemarkForm.Meta.widgets,
            ** {
                'sample_code': forms.TextInput(attrs={
                    'class': 'form-control',
                }),
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
            },
        )