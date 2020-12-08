from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save

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
        self.update()

@receiver(signal=post_save, sender=Request)
def send_email_after_save(sender, instance, **kwargs):
    slot = Slot.objects.get(id=instance.slot.id)
    initial_slot_status = slot.status
    initial_request_status = instance.status

    # try:
    if instance.status == Request.STATUS_1:
        slot.update_status(Slot.STATUS_2)
        subject = "Waiting for Faculty Approval"
        text = "Test Email send to {} : Faculty".format(instance.faculty.username)
        instance.faculty.send_email(subject, text, instance)

        subject = "Pending Lab Booking Request"
        text = "Test Email send to {} : Student".format(instance.student.username)
        receiver = instance.student.send_email(subject, text, instance)

    elif instance.status == Request.STATUS_2:
        if instance.message == 'accept':
            subject = "Waiting for Lab Assistant Approval"
            text = "Test Email send to {} : Lab Assistant".format(instance.lab_assistant.username)
            instance.lab_assistant.send_email(subject, text, instance)

        elif instance.message == 'reject':
            slot.update_status(Slot.STATUS_1)
            instance.update_status(Request.STATUS_5)

            subject = "Booking Rejected by {}".format(instance.faculty.username)
            text = "Test Email send to {} : Student".format(instance.student.username)
            receiver = instance.student.send_email(subject, text, instance)

    elif instance.status == Request.STATUS_3:
        if instance.message == 'accept':
            slot.update_status(Slot.STATUS_3)
            subject = "Lab Booking Approved"
            text = "Test Email for Booking Approved {}".format(instance.student.username)
            instance.student.send_email(subject, text, instance)

        elif instance.message == 'reject':
            slot.update_status(Slot.STATUS_1)
            instance.update_status(Request.STATUS_5)
            subject = "Booking Rejected by {}".format(instance.lab_assistant.username)
            text = "Test Email for Booking Rejected {}".format(instance.student.username)
            instance.student.send_email(subject, text, instance)

    # except:
    #     print("Failed Email Attempt. Reverting back to initial Slot and Request status")
    #     slot.update_status(initial_slot_status)
    #     if instance.status == Request.STATUS_1:
    #         print ("deleting instance {} {}".format(instance.id, instance))
    #         EmailModel.objects.filter(request=instance).delete()
    #         instance.delete()
    #     else:
    #         print (initial_request_status)
    #         print ("Updating Request object ")
    #         print (instance.status)
    #         Request.objects.filter(id=instance.id).update(
    #             status=initial_request_status
    #         )
    #         print (instance.status)
    #         # instance.update_status(initial_request_status)
