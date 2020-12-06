from django import forms

from ..models.user import Faculty, Student
from ..models.instrument.userdetails import UserDetail

class MyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "{} ({})".format(obj.name, obj.email)


class UserDetailsForm(forms.ModelForm):

    user_name = MyModelChoiceField(queryset=Student.objects.all(),
                                   widget=forms.Select(attrs={
                                                         'class': 'form-control',
                                                        }
                                    ))

    sup_name = MyModelChoiceField(queryset=Faculty.objects.all(),
                                  widget=forms.Select(attrs={
                                                        'class': 'form-control',
                                                      }
                                 ))

    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs['disabled'] = True
        self.fields['sup_name'].widget.attrs['disabled'] = True
        self.fields['date'].widget.attrs['disabled'] = True
        self.fields['sup_dept'].widget.attrs['readonly'] = True

    class Meta:
        model = UserDetail
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
            'date': forms.SelectDateWidget(attrs={
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