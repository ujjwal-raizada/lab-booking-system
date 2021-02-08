import calendar
from datetime import datetime
from django.db import models


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
    ## TODO: Update Duration to TimeField
    instrument = models.ForeignKey("Instrument", on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    ## Remove date and time and combine it to DateTimeField

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
    def duration(self):
        now_date = datetime.now().date()
        end_datetime = datetime.combine(now_date, self.end_time)
        start_datetime = datetime.combine(now_date, self.start_time)
        return end_datetime - start_datetime

    @property
    def duration_verbose(self):
        hours, reminder = divmod(self.duration.total_seconds(), 3600)
        minutes, seconds = divmod(reminder, 60)
        hours = f"{int(hours)} hr" if hours > 0 else ""
        minutes = f"{int(minutes)} min" if minutes > 0 else ""
        return " ".join((hours, minutes)).strip()

    @property
    def description(self):
        return "{} {} {} - {} to {} (Duration: {})".format(
            str(self.date.day),
            calendar.month_name[self.date.month],
            str(self.date.year),
            str(self.start_time),
            str(self.end_time),
            self.duration_verbose,
        )

    def __str__(self):
        return "{} : {}".format(self.instrument, self.description)
