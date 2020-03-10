from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from onlineCAL.settings import EMAIL_HOST_USER

class CustomUser(AbstractUser):

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
    name = models.CharField(max_length=50, unique=True, null=False)
    desc = models.CharField(max_length=200, null=True)

    @property
    def short_id(self):
        return self.name

    def __str__(self):
        return f"{self.name}"


class Slot(models.Model):
    STATUS_1 = "S1"
    STATUS_2 = "S2"
    STATUS_3 = "S3"
    STATUS_4 = "S4"

    STATUS_CHOICES = [
        (STATUS_1, "Empty"),
        (STATUS_2, "In Process"),
        (STATUS_3, "Filled"),
        (STATUS_4, "Passed")
    ]
    slot_name = models.CharField(max_length=50)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date = models.DateField()
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{str(self.date) + ' ' + str(self.time)}"


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
                                      default=None, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)


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
        print ("Attribute Error Called")

    def init_mail_and_send(recvr, request, mail_text, subject):
        EmailModel(receiver=recvr,
                   request=request,
                   text=mail_text,
                   subject=subject).save()

        try:
            send_mail(subject, mail_text, EMAIL_HOST_USER,
                     [receiver], fail_silently=False)
        except:
            slot.status = initial_status
            slot.save(update_fields=['status'])
            raise FailedEmailAttempt()

    def update_slot_status(status):
        assert status in (Slot.STATUS_1, Slot.STATUS_2, Slot.STATUS_3, Slot.STATUS_4), FailedEmailAttempt()
        slot.status = status
        slot.save(update_fields=['status'])

    def update_request_status(status):
        instance.status = status
        instance.save(update_fields=['status'])

    try:
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

    except FailedEmailAttempt:
        update_slot_status(initial_status)

    except Exception as e:
        print(e)
