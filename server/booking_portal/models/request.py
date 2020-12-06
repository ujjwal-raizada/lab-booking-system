from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .instrument import Instrument
from .slot import Slot
from .user import Student, Faculty, LabAssistant

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