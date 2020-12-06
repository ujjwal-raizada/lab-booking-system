from django.db import models
import datetime
import calendar

from .userdetails import UserDetail

class FESEM(UserDetail):
    sample_code = models.CharField(max_length=75)
    sample_nature = models.CharField(max_length=15, choices=[
                                                        ('Metal', 'Metal'),
                                                        ('Film', 'Film'),
                                                        ('Crystal', 'Crystal'),
                                                        ('Powder', 'Powder'),
                                                        ('Biological', 'Biological'),
                                                        ('Ceramic', 'Ceramic'),
                                                        ('Tissue', 'Tissue'),
                                                        ('Others', 'Others'),
                                                    ])
    analysis_nature = models.CharField(max_length=75)
    sputter_required = models.CharField(max_length=3, choices=[
                                                          ('Yes', 'Yes'),
                                                          ('No', 'No'),
                                                      ])
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'FESEM'
        verbose_name_plural = 'FESEM'


class TCSPC(UserDetail):
    sample_code = models.CharField(max_length=75)
    sample_nature = models.CharField(max_length=15, choices=[
                                                        ('Metal', 'Metal'),
                                                        ('Film', 'Film'),
                                                        ('Crystal', 'Crystal'),
                                                        ('Powder', 'Powder'),
                                                        ('Biological', 'Biological'),
                                                        ('Ceramic', 'Ceramic'),
                                                        ('Tissue', 'Tissue'),
                                                        ('Others', 'Others'),
                                                    ])
    chemical_composition = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'TCSPC'
        verbose_name_plural = 'TCSPC'


class FTIR(UserDetail):
    sample_code = models.CharField(max_length=75)
    composition = models.CharField(max_length=75)
    state = models.CharField(max_length=10, choices=[
                                                ('Solid', 'Solid'),
                                                ('Liquid', 'Liquid'),
                                            ])
    solvent = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'FTIR'
        verbose_name_plural = 'FTIR'


class LCMS(UserDetail):
    sample_code = models.CharField(max_length=75)
    composition = models.CharField(max_length=75)
    phase = models.CharField(max_length=75)
    no_of_lc_peaks = models.IntegerField()
    solvent_solubility = models.CharField(max_length=75)
    exact_mass = models.CharField(max_length=75)
    mass_adducts = models.CharField(max_length=75)
    analysis_mode = models.CharField(max_length=10, choices=[
                                                        ('Positive', 'Positive'),
                                                        ('Negative', 'Negative'),
                                                    ])
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'LCMS'
        verbose_name_plural = 'LCMS'


class Rheometer(UserDetail):
    sample_code = models.CharField(max_length=75)
    ingredient_details = models.CharField(max_length=75)
    physical_characteristics = models.CharField(max_length=75)
    chemical_nature = models.CharField(max_length=75)
    origin = models.CharField(max_length=10, choices=[
                                                ('Natural', 'Natural'),
                                                ('Synthetic', 'Synthetic')
                                             ])
    analysis_required = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'Rheometer'
        verbose_name_plural = 'Rheometer'


class AAS(UserDetail):
    sample_code = models.CharField(max_length=75)
    elements = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'AAS'
        verbose_name_plural = 'AAS'


class TGA(UserDetail):
    sample_code = models.CharField(max_length=75)
    chemical_composition = models.CharField(max_length=75)
    sample_amount = models.CharField(max_length=75)
    heating_program = models.CharField(max_length=15, choices=[
                                                        ('Dynamic', 'Dynamic'),
                                                        ('Isothermal', 'Isothermal'),
                                                      ])
    temperature = models.CharField(max_length=75)
    atmosphere = models.CharField(max_length=5, choices=[
                                                    ('N2', 'N2'),
                                                    ('Ar', 'Ar'),
                                                    ('Air', 'Air'),
                                                ])
    heating_rate = models.CharField(max_length=75)
    sample_solubility = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'TGA'
        verbose_name_plural = 'TGA'


class BET(UserDetail):
    sample_code = models.CharField(max_length=75)
    pretreatment_conditions = models.CharField(max_length=75)
    precautions = models.CharField(max_length=75)
    adsorption = models.CharField(max_length=75)
    surface_area = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'BET'
        verbose_name_plural = 'BET'


class CDSpectrophotometer(UserDetail):
    sample_code = models.CharField(max_length=75)
    wavelength_scan_start = models.CharField(max_length=75)
    wavelength_scan_end = models.CharField(max_length=75)
    wavelength_fixed = models.CharField(max_length=75)
    temp_range_scan_start = models.CharField(max_length=75)
    temp_range_scan_end = models.CharField(max_length=75)
    temp_range_fixed = models.CharField(max_length=75)
    concentration = models.CharField(max_length=75)
    cell_path_length = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'CDSpectrophotometer'
        verbose_name_plural = 'CDSpectrophotometer'


class LSCM(UserDetail):
    sample_description = models.CharField(max_length=75)
    dye = models.CharField(max_length=75)
    excitation_wavelength = models.CharField(max_length=75)
    emission_range = models.CharField(max_length=75)
    analysis_details = models.CharField(max_length=75)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'LSCM'
        verbose_name_plural = 'LSCM'


class DSC(UserDetail):
    sample_code = models.CharField(max_length=75)
    chemical_composition = models.CharField(max_length=75)
    sample_amount = models.CharField(max_length=75)
    heating_program = models.CharField(max_length=15, choices=[
                                                        ('Dynamic', 'Dynamic'),
                                                        ('Isothermal', 'Isothermal')
                                                      ])
    temp_range = models.CharField(max_length=75)
    atmosphere = models.CharField(max_length=5, choices=[
                                                    ('N2', 'N2'),
                                                    ('Ar', 'Ar'),
                                                    ('Air', 'Air'),
                                                ])
    heating_rate = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'DSC'
        verbose_name_plural = 'DSC'


class GC(UserDetail):
    sample_code = models.CharField(max_length=75)
    appearance = models.CharField(max_length=75)
    no_of_gc_peaks = models.IntegerField()
    solvent_solubility = models.CharField(max_length=75)
    column_details = models.CharField(max_length=75)
    exp_mol_wt = models.CharField(max_length=75)
    mp_bp = models.CharField(max_length=75)
    sample_source = models.CharField(max_length=15, choices=[
                                                        ('Natural', 'Natural'),
                                                        ('Synthesis', 'Synthesis'),
                                                        ('Waste', 'Waste')
                                                    ])
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'GC'
        verbose_name_plural = 'GC'


class EDXRF(UserDetail):
    sample_code = models.CharField(max_length=75)
    sample_nature = models.CharField(max_length=15, choices=[
                                                        ('Powder', 'Powder'),
                                                        ('Metal', 'Metal'),
                                                        ('Film', 'Film'),
                                                        ('Biological', 'Biological'),
                                                        ('Concrete', 'Concrete'),
                                                    ])
    elements_present = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'EDXRF'
        verbose_name_plural = 'EDXRF'


class HPLC(UserDetail):
    sample_code = models.CharField(max_length=75)
    sample_information = models.CharField(max_length=75)
    mobile_phase = models.CharField(max_length=75)
    column_for_lc = models.CharField(max_length=75)
    detection_wavelength = models.CharField(max_length=75)
    other_information = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'HPLC'
        verbose_name_plural = 'HPLC'


class NMR(UserDetail):
    sample_code = models.CharField(max_length=75)
    sample_nature = models.CharField(max_length=10, choices=[
                                                        ('Solid', 'Solid'),
                                                        ('Liquid', 'Liquid'),
                                                    ])
    quantity = models.CharField(max_length=75)
    solvent = models.CharField(max_length=75)
    analysis = models.CharField(max_length=75)
    experiment = models.CharField(max_length=75)
    spectral_range = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'NMR'
        verbose_name_plural = 'NMR'


class PXRD(UserDetail):
    sample_code = models.CharField(max_length=75)
    chemical_composition = models.CharField(max_length=75)
    sample_description = models.CharField(max_length=10, choices=[
                                                            ('Film', 'Film'),
                                                            ('Powder', 'Powder'),
                                                            ('Pellet', 'Pellet'),
                                                         ])
    range = models.CharField(max_length=75)
    scanning_rate = models.CharField(max_length=75)
    any_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'PXRD'
        verbose_name_plural = 'PXRD'


class SCXRD(UserDetail):
    sample_code = models.CharField(max_length=75)
    chemical_composition = models.CharField(max_length=75)
    scanning_rate = models.CharField(max_length=75)
    source = models.CharField(max_length=5, choices=[
                                                ('Cu', 'Cu'),
                                                ('Mo', 'Mo'),
                                            ])
    any_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'SCXRD'
        verbose_name_plural = 'SCXRD'


class XPS(UserDetail):
    sample_name = models.CharField(max_length=75)
    sample_nature = models.CharField(max_length=75)
    chemical_composition = models.CharField(max_length=75)
    sample_property = models.CharField(max_length=20, choices=[
                                                        ('Conducting', 'Conducting'),
                                                        ('Semi Conducting', 'Semi Conducting'),
                                                        ('Insulating', 'Insulating'),
                                                      ])
    analysed_elements = models.CharField(max_length=75)
    scan_details = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'XPS'
        verbose_name_plural = 'XPS'


class UVSpectrophotometer(UserDetail):
    sample_code = models.CharField(max_length=75)
    sample_composition = models.CharField(max_length=75)
    molecular_weight = models.CharField(max_length=75)
    analysis_mode = models.CharField(max_length=10, choices=[
                                                        ('Solid', 'Solid'),
                                                        ('Liquid', 'Liquid'),
                                                        ('Thin Film', 'Thin Film'),
                                                    ])
    wavelength = models.CharField(max_length=75)
    ordinate_mode = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'UVSpectrophotometer'
        verbose_name_plural = 'UVSpectrophotometer'