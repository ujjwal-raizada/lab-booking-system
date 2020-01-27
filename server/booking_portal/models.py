from django.db import models
from django.contrib.auth.models import AbstractUser


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
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200, null=True)


class Slot(models.Model):
    STATUS_CHOICES = [
        ("S1", "Empty"),
        ("S2", "In Process"),
        ("S3", "Filled"),
        ("S4", "Passed")
    ]
    slot_name = models.CharField(max_length=50)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date = models.DateField()
    time = models.TimeField(null=True)


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
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT, null=True)
    request = models.ForeignKey(Request, on_delete=models.PROTECT, null=True)
    text = models.CharField(max_length=500)
    date_time = models.DateTimeField()
