from django import forms
from .userform import UserForm


class FESEMForm(UserForm):
    sample_code = forms.CharField(label="Sample Code", max_length=50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    sample_nature = forms.ChoiceField(label="Nature of Sample",choices=[
                                        ('Metal', 'Metal'),
                                        ('Film', 'Film'),
                                        ('Crystal', 'Crystal'),
                                        ('Powder', 'Powder'),
                                        ('Biological', 'Biological'),
                                        ('Ceramic', 'Ceramic'),
                                        ('Tissue', 'Tissue'),
                                        ('Others', 'Others'),
                                        ], widget=forms.Select(
                                                attrs={
                                                    'class': 'form-control',
                                                }
    ))

    analysis_nature = forms.CharField(label="Nature of Analysis (SEM EDX STEM etc.)", max_length=50, widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                        }
    ))
    
    sputter_required = forms.ChoiceField(label="Sputter Coating Required", choices=[
                                            ('Yes', 'Yes'),
                                            ('No', 'No'),
                                            ], widget=forms.Select(
                                                attrs={
                                                    'class': 'form-control',
                                                }
    ))

    other_remarks = forms.CharField(label="Any Other Remarks", widget=forms.Textarea(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))