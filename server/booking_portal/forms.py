from django import forms

class UserForm(forms.Form):
    user_name = forms.CharField(label="User Name", max_length=75, widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                }
    ))

    date = forms.DateField(widget=forms.SelectDateWidget(
                            attrs={
                                'class': 'custom-select m-3',
                            }
    ))

    sup_name = forms.CharField(label="Supervisor Name", max_length=75, widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                }
    ))

    sup_dept = forms.CharField(label="Supervisor Department", max_length=75, widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                }
    ))

    sample_from_outside = forms.ChoiceField(label="Is the sample from outside BITS obtained through collaboration?", choices = [
                                            ('Yes', 'Yes'),
                                            ('No', 'No'),
                                            ], widget=forms.Select(
                                                attrs = {
                                                    'class': 'form-control',
                                                }
    ))

    origin_of_sample = forms.CharField(label="Provide origin of the sample", max_length=75, widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                        }
    ))


class FESEMForm(UserForm):
    req_discussed = forms.ChoiceField(label="Have sampling modalities and requirements discussed with the operator?", choices = [
                                        ('Yes', 'Yes'),
                                        ('No', 'No'),
                                        ], widget=forms.Select(
                                                attrs = {
                                                    'class': 'form-control',
                                                }
    ))

    sample_code = forms.CharField(label="Sample Code", max_length = 50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    sample_nature = forms.ChoiceField(label = "Nature of Sample",choices = [
                                        ('Metal', 'Metal'),
                                        ('Film', 'Film'),
                                        ('Crystal', 'Crystal'),
                                        ('Powder', 'Powder'),
                                        ('Biological', 'Biological'),
                                        ('Ceramic', 'Ceramic'),
                                        ('Tissue', 'Tissue'),
                                        ('Others', 'Others'),
                                        ], widget=forms.Select(
                                                attrs = {
                                                    'class': 'form-control',
                                                }
    ))

    analysis_nature = forms.CharField(label = "Nature of Analysis (SEM EDX STEM etc.)", max_length = 50, widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                        }
    ))
    
    sputter_required = forms.ChoiceField(label = "Sputter Coating Required", choices = [
                                            ('Yes', 'Yes'),
                                            ('No', 'No'),
                                            ], widget=forms.Select(
                                                attrs = {
                                                    'class': 'form-control',
                                                }
    ))

    other_remarks = forms.CharField(label="Enter any other remarks", widget=forms.Textarea(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))