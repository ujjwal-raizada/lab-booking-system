from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.utils import timezone

from .manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy("email address"), unique=True, max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def username(self):
        return self.email

    def __str__(self):
        return "{} ({})".format(self.name, self.email[:self.email.find("@")].lower())


class Faculty(CustomUser):
    department = models.CharField(max_length=20, null=False)

    class Meta:
        verbose_name = "faculty"
        verbose_name_plural = "faculties"
        default_related_name = "faculties"


class Student(CustomUser):
    supervisor = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=False)

    class Meta:
        verbose_name = "student"
        default_related_name = "students"


class LabAssistant(CustomUser):
    class Meta:
        verbose_name = "lab assistant"
        default_related_name = "labassistants"
