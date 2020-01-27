from django import forms
from .userform import UserForm


class LCMSForm(UserForm):
    sample_code = forms.CharField(label="Sample Code", max_length=50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    composition = forms.CharField(label="Sample Information / Composition", max_length=50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    phase = forms.CharField(label="Mobile Phase and Column for LC", max_length=75, widget=forms.TextInput(
                            attrs={
                                'class': 'form-control',
                            }
    ))

    no_of_lc_peaks = forms.IntegerField(label="No. of LC peaks", widget=forms.NumberInput(
                            attrs={
                                'class': 'form-control',
                            }
    ))

    solvent_solubility = forms.CharField(label="Solvent Solubility", max_length=50, widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control',
                                            }
    ))

    exact_mass = forms.CharField(label="Exact Mass", max_length=50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    mass_adducts = forms.CharField(label="Expected Mass Adducts", max_length=50, widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
    ))

    analysis_mode = forms.ChoiceField(label='Mode of Analysis (Positive / Negative)', choices=[
                                        ('Positive', 'Positive'),
                                        ('Negative', 'Negative'),
                                        ], widget=forms.Select(
                                            attrs={
                                                'class': 'form-control',
                                            }
    ))