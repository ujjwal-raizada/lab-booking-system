from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .slot import Slot
from .user import Student, Faculty, LabAssistant


class Request(models.Model):
    WAITING_FOR_FACULTY = "R1"
    WAITING_FOR_LAB_ASST = "R2"
    APPROVED = "R3"
    REJECTED = "R4"
    CANCELLED = "R5"

    STATUS_CHOICES = [
        (WAITING_FOR_FACULTY, "Waiting for faculty approval."),
        (WAITING_FOR_LAB_ASST, "Waiting for lab assistant approval."),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (CANCELLED, "Cancelled")
    ]
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    lab_assistant = models.ForeignKey(LabAssistant, on_delete=models.PROTECT,
                                      blank=True, null=True)
    instrument = models.ForeignKey("Instrument", on_delete=models.PROTECT)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    ## To keep a reference of different form types
    ## against a request
    content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def update_status(self, status):
        assert status in (
            Request.WAITING_FOR_FACULTY,
            Request.WAITING_FOR_LAB_ASST,
            Request.APPROVED,
            Request.REJECTED,
            Request.CANCELLED,
        )
        self.status = status
        self.save(update_fields=['status'])

    def __str__(self):
        return "Request: {}".format(self.slot)


@receiver(signal=post_save, sender=Request)
def send_email_after_save(sender, instance, **kwargs):
    slot = Slot.objects.get(id=instance.slot.id)

    if instance.status == Request.WAITING_FOR_FACULTY:
        slot.update_status(Slot.STATUS_2)
        subject = "Waiting for Faculty Approval"
        text = render_to_string('email/faculty_pending.html', {
            'receipent_name': instance.faculty.name,
            'student_name': instance.student.name,
            'instrument_name': instance.instrument.name,
            'slot': instance.slot.description,
        })
        instance.faculty.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)

        subject = "Pending Lab Booking Request"
        text = render_to_string('email/student_pending.html', {
            'receipent_name': instance.student.name,
            'instrument_name': instance.instrument.name,
            'slot': instance.slot.description,
        })
        instance.student.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)

    elif instance.status == Request.WAITING_FOR_LAB_ASST:
        subject = "Waiting for Lab Assistant Approval"
        text = render_to_string('email/lab_assistant_pending.html', {
            'receipent_name': instance.lab_assistant.name,
            'student_name': instance.student.name,
            'instrument_name': instance.instrument.name,
            'faculty_name': instance.faculty.name,
            'slot': instance.slot.description,
        })
        instance.lab_assistant.send_email(instance, subject,
                                          strip_tags(text),
                                          html_message=text)

    elif instance.status == Request.APPROVED:
        slot.update_status(Slot.STATUS_3)
        subject = "Lab Booking Approved"
        text = render_to_string('email/student_accepted.html', {
            'receipent_name': instance.student.name,
            'slot': instance.slot.description,
        })
        instance.student.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)

    elif instance.status == Request.REJECTED:
        slot.update_status(Slot.STATUS_1)
        subject = "Lab Booking Rejected"
        text = render_to_string('email/student_rejected.html', {
            'receipent_name': instance.student.name,
            'slot': instance.slot.description,
            'faculty_remarks': instance.content_object.faculty_remarks,
            'lab_assistant_remarks': instance.content_object.lab_assistant_remarks,
        })
        instance.student.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)

    elif instance.status == Request.CANCELLED:
        subject = "Lab Booking Cancelled"
        text = render_to_string('email/student_rejected.html', {
            'receipent_name': instance.student.name,
            'slot': instance.slot.description,
            'faculty_remarks': instance.content_object.faculty_remarks,
            'lab_assistant_remarks': instance.content_object.lab_assistant_remarks,
        })
        instance.student.send_email(instance, subject,
                                    strip_tags(text),
                                    html_message=text)
