from django.db import models
from django.core.mail import send_mail

from .slot import Slot

class EmailModel(models.Model):
    receiver = models.EmailField(null=True, blank=False)
    request = models.ForeignKey("Request", on_delete=models.PROTECT, null=True, blank=False)
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