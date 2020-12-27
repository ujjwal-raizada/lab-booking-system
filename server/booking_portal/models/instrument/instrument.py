import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from .. import Slot, Request


class Instrument(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    desc = models.CharField(max_length=200, null=True)
    status = models.BooleanField(
        help_text="'No' will cancel all pending requests and slots for this machine",
        verbose_name="Available for Booking?",
        default=True,
    )

    @property
    def short_id(self):
        return self.name

    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=Instrument)
def handle_requests(sender, instance, **kwargs):
    if instance.status:
        for slot in Slot.objects.filter(
            instrument=instance,
            date__gte=datetime.datetime.today(),
            status=Slot.STATUS_4,
        ):
            slot.status = Slot.STATUS_1
            slot.save()
    else:
        slot_objects = Slot.objects.filter(
            instrument=instance,
            date__gte=datetime.datetime.today(),
        )

        req_objects = Request.objects.filter(
            instrument=instance,
            slot__date__gte=datetime.datetime.today(),
        )

        for slot in slot_objects:
            slot.status = Slot.STATUS_4
            slot.save()

        for req in req_objects:
            req.status = Request.STATUS_5

            previous_remarks = req.content_object.lab_assistant_remarks
            new_remarks = "This slot has been cancelled due to technical/maintainence reasons."
            if previous_remarks is not None:
                new_remarks = previous_remarks + '\n' + new_remarks

            req.content_object.lab_assistant_remarks = new_remarks
            req.content_object.save()
            req.save()
