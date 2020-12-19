from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    desc = models.CharField(max_length=200, null=True)

    @property
    def short_id(self):
        return self.name

    def __str__(self):
        return f"{self.name}"
