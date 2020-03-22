from django import forms

from ..models import AAS
from .userform import UserDetailsForm


class AASForm(UserDetailsForm):
    class Meta(UserDetailsForm.Meta):
        model = AAS
        fields = UserDetailsForm.Meta.fields + ('sample_code', 
                                                'elements',
                                                'other_remarks')
        UserDetailsForm.Meta.labels.update(
            {
                'sample_code': 'Sample Code',
                'elements': 'Elements to be Analyzed',
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
                'elements': forms.TextInput(attrs={
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