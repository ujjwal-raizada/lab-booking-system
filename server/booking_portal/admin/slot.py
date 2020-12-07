import csv
import datetime
from io import TextIOWrapper

from django.urls import path
from django.contrib import admin
from django.shortcuts import render, redirect

from ..models import Instrument, Slot
from ..forms.adminForms import BulkTimeSlotForm

class SlotAdmin(admin.ModelAdmin):
    change_list_template = "admin/slot_change_list.html"

    def time_left(self, current, end, duration):
        today = datetime.date.today()
        diff = (datetime.datetime.combine(today, end) -
                datetime.datetime.combine(today, current))

        return (diff >= duration)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-slot/", self.generate_slots),
        ]
        return my_urls + urls

    def generate_slots(self, request):
        INTERVAL_CHOICES = {
                "1-hour" : datetime.timedelta(hours=1),
                "2-hour" : datetime.timedelta(hours=2),
                '4-hour' : datetime.timedelta(hours=4),
                '3-hour' : datetime.timedelta(hours=3),
            }

        if request.method == 'POST':
            today = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
            start_time = int(request.POST.get('start_time').split(':')[0])
            end_time = int(request.POST.get('end_time').split(':')[0])
            instr = Instrument.objects.get(id=request.POST.get('instruments'))
            duration = INTERVAL_CHOICES.get(request.POST.get('lab_duration'), None)
            delta = int(request.POST.get('for_the_next'))

            if start_time >= end_time: return redirect('..')
            if duration == None: return redirect('..')
            if today.date() < datetime.date.today(): return redirect('..')

            today_weekday = today.weekday()
            next_days = [today + datetime.timedelta(days=var) for var in range(0, delta)]

            all_slots = {}
            for day in next_days:
                day_wise = []
                current = datetime.time(hour=start_time)
                end = datetime.time(hour=end_time)
                while current < end and self.time_left(current, end, duration) == True:
                    day_wise.append(datetime.datetime.combine(day, current))
                    current = datetime.time(hour=(datetime.datetime.combine(day, current) + duration).hour)
                all_slots[day] = day_wise

            for day, time_slots in all_slots.items():
                for time_slot in time_slots:
                    if not Slot.objects.filter(instrument=instr, date=day, time=time_slot.time()).exists():
                        slot_obj = Slot(slot_name=instr.name, instrument=instr,
                                        status=Slot.STATUS_1, date=day, time=time_slot.time())
                        slot_obj.save()

            return redirect("..")
        form = BulkTimeSlotForm()
        payload = {"form": form}
        return render(
            request, "admin/bulk_import_slots_form.html", payload
        )