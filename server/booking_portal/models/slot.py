import calendar
from django.db import models

from .instrument import Instrument

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

    def update_status(self, status):
        assert status in (
                Slot.STATUS_1,
                Slot.STATUS_2,
                Slot.STATUS_3,
                Slot.STATUS_4
        )
        self.status = status
        self.save(update_fields=['status'])

    @property
    def description(self):
        return "{} {} {} - {}".format(
            str(self.date.day),
            calendar.month_name[self.date.month],
            str(self.date.year),
            str(self.time)
        )

    def __str__(self):
        return "{} : {}".format(self.instrument, self.description)
