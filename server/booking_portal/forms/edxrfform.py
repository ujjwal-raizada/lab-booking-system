from django import forms

from ..models.instrument.form_models import EDXRF
from .userform import UserDetailsForm


class EDXRFForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = EDXRF
        fields = UserDetailsForm.Meta.fields + ('sample_code',
                                                'sample_nature',
                                                'elements_present',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'sample_nature': 'Nature of Sample',
                'elements_present': 'Elements Present',
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
                'elements_present': forms.TextInput(attrs={
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