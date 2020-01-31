# Generated by Django 3.0.2 on 2020-01-31 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_portal', '0003_auto_20200127_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailmodel',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='emailmodel',
            name='instrument',
        ),
        migrations.RemoveField(
            model_name='emailmodel',
            name='student',
        ),
        migrations.AddField(
            model_name='emailmodel',
            name='receiver',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='emailmodel',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='emailmodel',
            name='text',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
