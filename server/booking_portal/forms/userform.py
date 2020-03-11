from django import forms

from ..models import UserDetails


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('user_name',
                  'date',
                  'sup_name',
                  'sup_dept',
                  'sample_from_outside',
                  'origin_of_sample',
                  'req_discussed')
        labels = {
            'user_name': 'Username',
            'sup_name': 'Supervisor Name',
            'sup_dept': 'Supervisor Department',
            'sample_from_outside': 'Is the sample obtained from outside BITS through collaboration?',
            'origin_of_sample': 'Provide origin of sample',
            'req_discussed': 'Have the sampling modalities and requirements been discussed with the operator?',
        }
        widgets = {
            'user_name': forms.TextInput(attrs={
                                           'class': 'form-control',
                                         }
            ),
            'date': forms.SelectDateWidget(attrs={
                                              'class': 'form-control',
                                           }
            ),
            'sup_name': forms.TextInput(attrs={
                                           'class': 'form-control',
                                        }
            ),
            'sup_dept': forms.TextInput(attrs={
                                           'class': 'form-control',
                                        }
            ),
            'sample_from_outside': forms.Select(attrs={
                                                   'class': 'form-control',
                                                }
            ),
            'origin_of_sample': forms.TextInput(attrs={
                                                   'class': 'form-control',
                                                }
            ),
            'req_discussed': forms.Select(attrs={
                                             'class': 'form-control',
                                          }
            ),
        }