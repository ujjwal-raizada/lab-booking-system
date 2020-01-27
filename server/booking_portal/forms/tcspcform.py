from django import forms
from .userform import UserForm


class TCSPCForm(UserForm):
    sample_code = forms.CharField(label='Sample Code', max_length=50, widget=forms.TextInput(
                                    attrs = {
                                        "class": "form-control",
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

    chemical_composition = forms.CharField(label="Chemical Composition", max_length=50, widget=forms.TextInput(
                                            attrs={
                                                "class": "form-control",
                                            }
    ))

    other_remarks = forms.CharField(label='Any Other Remarks', max_length=75, widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                    }
    ))