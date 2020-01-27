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


class EmailModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    text = models.CharField(max_length=500)
    date_time = models.DateTimeField()
