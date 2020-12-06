from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from .request import Request
from .slot import Slot
from onlineCAL.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


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

class FailedEmailAttempt(Exception):
    def __str__(self):
        return "Attempt to Send Email failed !"


@receiver(signal=post_save, sender=Request)
def send_email_after_save(sender, instance, **kwargs):
    slot = Slot.objects.get(id=instance.slot.id)
    initial_status = slot.status
    try:
        message = instance.message
    except AttributeError:
        message = None
        print ("No Attribute present")

    def init_mail_and_send(recvr, request, mail_text, subject):
        EmailModel(receiver=recvr,
                   request=request,
                   text=mail_text,
                   subject=subject).save()

        # try:
        send_mail(subject, mail_text, EMAIL_HOST_USER,
                    [recvr], fail_silently=False)
        # except:
            # raise FailedEmailAttempt()

    def update_slot_status(status):
        assert status in (
            Slot.STATUS_1,
            Slot.STATUS_2,
            Slot.STATUS_3,
            Slot.STATUS_4), FailedEmailAttempt()
        slot.status = status
        slot.save(update_fields=['status'])

    def update_request_status(status):
        instance.status = status
        instance.save(update_fields=['status'])

    if instance.status == Request.STATUS_1:
        update_slot_status(Slot.STATUS_2) # in-process
        subject = "Waiting for Faculty Approval"
        text = "Test Email send to {} : Faculty".format(instance.faculty.username)
        receiver = instance.faculty.email
        init_mail_and_send(receiver, instance, text, subject)

        subject = "Pending Lab Booking Request"
        text = "Test Email send to {} : Student".format(instance.student.username)
        receiver = instance.student.email
        init_mail_and_send(receiver, instance, text, subject)

    elif instance.status == Request.STATUS_2:
        if message == 'accept':
            subject = "Waiting for Lab Assistant Approval"
            text = "Test Email send to {} : Lab Assistant".format(instance.lab_assistant.username)
            receiver = instance.lab_assistant.email
            init_mail_and_send(receiver, instance, text, subject)

        elif message == 'reject':
            update_slot_status(Slot.STATUS_1)
            update_request_status(Request.STATUS_5)
            subject = "Booking Rejected by {}".format(instance.faculty.username)
            text = "Test Email send to {} : Student".format(instance.student.username)
            receiver = instance.student.email
            init_mail_and_send(receiver, instance, text, subject)

    elif instance.status == Request.STATUS_3:
        if message == 'accept':
            update_slot_status(Slot.STATUS_3)
            subject = "Lab Booking Approved"
            text = "Test Email for Booking Approved {}".format(instance.student.username)
            receiver = instance.student.email
            init_mail_and_send(receiver, instance, text, subject)

        elif message == 'reject':
            update_slot_status(Slot.STATUS_1)
            update_request_status(Request.STATUS_5)
            subject = "Booking Rejected by {}".format(instance.lab_assistant.username)
            text = "Test Email for Booking Rejected {}".format(instance.student.username)
            receiver = instance.student.email
            init_mail_and_send(receiver, instance, text, subject)

    # except FailedEmailAttempt:
    #     print ("Failed Email Attempt")
    #     update_slot_status(initial_status)

    # except Exception as e:
    #     print(e)
