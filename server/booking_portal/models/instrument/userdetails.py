from django.db import models
import datetime
import calendar


class UserDetail(models.Model):
    user_name = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    sup_name = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    sup_dept = models.CharField(max_length=75)
    sample_from_outside = models.CharField(max_length=3, choices=[('Yes', 'Yes'),
                                                                  ('No', 'No')])
    origin_of_sample = models.CharField(max_length=75)
    req_discussed = models.CharField(max_length=3, choices=[('Yes', 'Yes'),
                                                            ('No', 'No')])

    def __str__(self):
        return 'Form ' + ": " +  str(self.date.day) + " " + calendar.month_name[self.date.month] + " " + str(self.date.year)

    class Meta:
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'