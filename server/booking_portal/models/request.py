from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

    def update_status(self, status):
        assert status in (
            Request.STATUS_1,
            Request.STATUS_2,
            Request.STATUS_3,
            Request.STATUS_4,
            Request.STATUS_5,
        )
        self.status = status
        self.save(update_fields=['status'])

    def __str__(self):
        return self.slot

@receiver(signal=post_save, sender=Request)
def send_email_after_save(sender, instance, **kwargs):
    slot = Slot.objects.get(id=instance.slot.id)

    if instance.status == Request.STATUS_1:
        slot.update_status(Slot.STATUS_2)
        subject = "Waiting for Faculty Approval"
        text = render_to_string('email/faculty_pending.html', {
            'receipent_name' : instance.faculty.name,
            'student_name' : instance.student.name,
            'instrument_name': instance.instrument.name,
            'slot' : instance.slot.description,
        })
        instance.faculty.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)

        subject = "Pending Lab Booking Request"
        text = render_to_string('email/student_pending.html', {
            'receipent_name' : instance.student.name,
            'instrument_name' : instance.instrument.name,
            'slot' : instance.slot.description,
        })
        instance.student.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)

    elif instance.status == Request.STATUS_2:
        subject = "Waiting for Lab Assistant Approval"
        text = render_to_string('email/lab_assistant_pending.html', {
            'receipent_name' : instance.lab_assistant.name,
            'student_name' : instance.student.name,
            'instrument_name' : instance.instrument.name,
            'faculty_name' : instance.faculty.name,
            'slot' : instance.slot.description,
        })
        instance.lab_assistant.send_email(instance, subject,
                                          strip_tags(text),
                                          html_message=text)

    elif instance.status == Request.STATUS_3:
        slot.update_status(Slot.STATUS_3)
        subject = "Lab Booking Approved"
        text = render_to_string('email/student_accepted.html', {
            'receipent_name' : instance.student.name,
            'slot' : instance.slot.description,
        })
        instance.student.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)

    elif instance.status == Request.STATUS_4:
        slot.update_status(Slot.STATUS_1)
        subject = "Lab Booking Rejected"
        text = render_to_string('email/student_rejected.html', {
            'receipent_name' : instance.student.name,
            'slot' : instance.slot.description,
        })
        instance.student.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)
