from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from onlineCAL.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

import datetime, calendar

class CustomUser(AbstractUser):

    name = models.CharField(max_length=50)

    @property
    def short_id(self):
        return self.username[:self.username.find("@")].lower()

    def __str__(self):
        return f"{self.name} ({self.short_id})"


class Student(CustomUser):
    id_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = "student"
        default_related_name = "students"


class Faculty(CustomUser):
    class Meta:
        verbose_name = "faculty"
        verbose_name_plural = "faculties"
        default_related_name = "faculties"


class LabAssistant(CustomUser):
    class Meta:
        verbose_name = "lab assistant"
        default_related_name = "labassistants"


class Instrument(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    desc = models.CharField(max_length=200, null=True)

    @property
    def short_id(self):
        return self.name

    def __str__(self):
        return f"{self.name}"


class Slot(models.Model):
    STATUS_1 = "S1"
    STATUS_2 = "S2"
    STATUS_3 = "S3"
    STATUS_4 = "S4"

    STATUS_CHOICES = [
        (STATUS_1, "Empty"),
        (STATUS_2, "In Process"),
        (STATUS_3, "Filled"),
        (STATUS_4, "Passed")
    ]
    slot_name = models.CharField(max_length=50)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date = models.DateField()
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{str(self.date) + ' ' + str(self.time)}"


class Request(models.Model):
    STATUS_1 = "R1"
    STATUS_2 = "R2"
    STATUS_3 = "R3"
    STATUS_4 = "R4"
    STATUS_5 = "R5"

    STATUS_CHOICES = [
        (STATUS_1, "Waiting for faculty approval."),
        (STATUS_2, "Waiting for lab assistant approval."),
        (STATUS_3, "Approved"),
        (STATUS_4, "Rejected"),
        (STATUS_5, "Cancelled")
    ]
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    lab_assistant = models.ForeignKey(LabAssistant, on_delete=models.PROTECT,
                                      blank=True, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class EmailModel(models.Model):
    receiver = models.EmailField(null=True, blank=False)
    request = models.ForeignKey(Request, on_delete=models.PROTECT, null=True, blank=False)
    date_time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500, null=True)
    subject = models.CharField(max_length=100, null=True)

    @property
    def short_id(self):
        return self.subject

    def __str__(self):
        return f"{self.subject}"


class FailedEmailAttempt(Exception):
    def __str__(self):
        return "Attempt to Send Email failed !"


@receiver(signal=post_save, sender=Request)
def send_email_after_save(sender, instance, **kwargs):
    slot = Slot.objects.get(id=instance.slot.id)
    initial_status = slot.status
    try:
        message = instance.message
    except AttributeError:
        message = None
        print ("No Attribute present")

    def init_mail_and_send(recvr, request, mail_text, subject):
        EmailModel(receiver=recvr,
                   request=request,
                   text=mail_text,
                   subject=subject).save()

        try:
            send_mail(subject, mail_text, EMAIL_HOST_USER,
                     [recvr], fail_silently=False)
        except:
            raise FailedEmailAttempt()

    def update_slot_status(status):
        assert status in (
            Slot.STATUS_1,
            Slot.STATUS_2,
            Slot.STATUS_3,
            Slot.STATUS_4), FailedEmailAttempt()
        slot.status = status
        slot.save(update_fields=['status'])

    def update_request_status(status):
        instance.status = status
        instance.save(update_fields=['status'])

    try:
        if instance.status == Request.STATUS_1:
            update_slot_status(Slot.STATUS_2) # in-process
            subject = "Waiting for Faculty Approval"
            text = "Test Email send to {} : Faculty".format(instance.faculty.username)
            receiver = instance.faculty.email
            init_mail_and_send(receiver, instance, text, subject)

            subject = "Pending Lab Booking Request"
            text = "Test Email send to {} : Student".format(instance.student.username)
            receiver = instance.student.email
            init_mail_and_send(receiver, instance, text, subject)

        elif instance.status == Request.STATUS_2:
            if message == 'accept':
                subject = "Waiting for Lab Assistant Approval"
                text = "Test Email send to {} : Lab Assistant".format(instance.lab_assistant.username)
                receiver = instance.lab_assistant.email
                init_mail_and_send(receiver, instance, text, subject)

            elif message == 'reject':
                update_slot_status(Slot.STATUS_1)
                update_request_status(Request.STATUS_5)
                subject = "Booking Rejected by {}".format(instance.faculty.username)
                text = "Test Email send to {} : Student".format(instance.student.username)
                receiver = instance.student.email
                init_mail_and_send(receiver, instance, text, subject)

        elif instance.status == Request.STATUS_3:
            if message == 'accept':
                update_slot_status(Slot.STATUS_3)
                subject = "Lab Booking Approved"
                text = "Test Email for Booking Approved {}".format(instance.student.username)
                receiver = instance.student.email
                init_mail_and_send(receiver, instance, text, subject)

            elif message == 'reject':
                update_slot_status(Slot.STATUS_1)
                update_request_status(Request.STATUS_5)
                subject = "Booking Rejected by {}".format(instance.lab_assistant.username)
                text = "Test Email for Booking Rejected {}".format(instance.student.username)
                receiver = instance.student.email
                init_mail_and_send(receiver, instance, text, subject)

    except FailedEmailAttempt:
        print ("Failed Email Attempt")
        update_slot_status(initial_status)

    except Exception as e:
        print(e)


class UserDetails(models.Model):
    user_name = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    sup_name = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    sup_dept = models.CharField(max_length=75)
    sample_from_outside = models.CharField(max_length=3, choices=[('Yes', 'Yes'),
                                                                  ('No', 'No')])
    origin_of_sample = models.CharField(max_length=75)
    req_discussed = models.CharField(max_length=3, choices=[('Yes', 'Yes'),
                                                            ('No', 'No')])

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'


class FESEM(UserDetails):
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


class TCSPC(UserDetails):
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


class FTIR(UserDetails):
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


class LCMS(UserDetails):
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


class Rheometer(UserDetails):
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


class AAS(UserDetails):
    sample_code = models.CharField(max_length=75)
    elements = models.CharField(max_length=75)
    other_remarks = models.CharField(max_length=200)

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'AAS'
        verbose_name_plural = 'AAS'


class TGA(UserDetails):
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


class BET(UserDetails):
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


class CDSpectrophotometer(UserDetails):
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


class LSCM(UserDetails):
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


class DSC(UserDetails):
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


class GC(UserDetails):
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


class EDXRF(UserDetails):
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


class HPLC(UserDetails):
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


class NMR(UserDetails):
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


class PXRD(UserDetails):
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


class SCXRD(UserDetails):
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


class XPS(UserDetails):
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


class UVSpectrophotometer(UserDetails):
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