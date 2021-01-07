from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from .manager import CustomUserManager
from .email import EmailModel


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy(
        "email address"), unique=True, max_length=50)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        
        if (self.is_superuser):
            return True
        if (
            self.is_staff and
            (
                'student' in perm or
                'faculty' in perm or
                'labassistant' in perm or
                'slot' in perm or
                'instrument' in perm or
                'announcement' in perm
            )):
            # Models accessible by lab assistants
            # TODO: Find a better way to add these permissions
            return True

        return False

    def has_module_perms(self, app_label):
        return self.is_staff

    def _create_email_obj(self, request, subject, message):
        EmailModel(receiver=self.email,
                   request=request,
                   text=message,
                   subject=subject).save()

    def send_email(self, request, subject, message, sender=None, html_message=None, **kwargs):
        self._create_email_obj(request, subject, message)
        sender = settings.EMAIL_HOST_USER if sender == None else sender

        # set 'fail_silently=False' when debugging the email system.
        send_mail(subject, message, sender, [self.email],
                  html_message=html_message, fail_silently=True)

    @property
    def username(self):
        return self.email

    def __str__(self):
        return "{} ({})".format(self.name, self.email[:self.email.find("@")].lower())


class Faculty(CustomUser):
    department = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = "faculty"
        verbose_name_plural = "faculties"
        default_related_name = "faculties"


class Student(CustomUser):
    supervisor = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, null=False)

    class Meta:
        verbose_name = "student"
        default_related_name = "students"


class LabAssistant(CustomUser):
    class Meta:
        verbose_name = "lab assistant"
        default_related_name = "labassistants"
