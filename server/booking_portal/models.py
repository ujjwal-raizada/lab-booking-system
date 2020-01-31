from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from onlineCAL.settings import EMAIL_HOST_USER

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField("email address", unique=True, primary_key=True)
    name = models.CharField(max_length=50)

    @property
    def short_id(self):
        return self.email[:self.email.find("@")].lower()

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
        return f"{self.date, self.time}"


class Request(models.Model):
    STATUS_CHOICES = [
        ("S1", "Waiting for faculty approval."),
        ("S2", "Waiting for lab assistant approval."),
        ("S3", "Approved"),
        ("S4", "Rejected"),
        ("S5", "Cancelled")
    ]
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)


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


@receiver(signal=post_save, sender=EmailModel)
def send_email_after_save(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    subject = instance.subject
    text = instance.text

    send_mail(subject, text, EMAIL_HOST_USER, [receiver], fail_silently=False)
