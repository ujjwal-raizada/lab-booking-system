from django import forms
from .userform import UserForm


class FTIRForm(UserForm):
    sample_code = forms.CharField(label="Sample Code", max_length=50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    composition = forms.CharField(label="Composition", max_length=50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    state = forms.ChoiceField(label="Solid / Liquid", choices=[
                                ("Solid", "Solid"),
                                ("Liquid", "Liquid")
                                ], widget=forms.Select(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    solvent = forms.CharField(label="Solvent Used (if any)", max_length=50, widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                }
    ))

    other_remarks = forms.CharField(label="Any Other Relevant Information", max_length=50, widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                }
    ))