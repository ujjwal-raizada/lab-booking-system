import datetime

from django.contrib import admin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.translation import gettext_lazy
from rangefilter.filter import DateRangeFilter

from ..forms.adminForms import BulkTimeSlotForm
from ..models import Instrument, Slot


class SlotFilterByInstrument(admin.SimpleListFilter):
    # Name to be displayed on the admin portal
    title = gettext_lazy("Instrument")

    parameter_name = 'instrument'

    def lookups(self, request, model_admin):
        """Returns a list of tuples. The first element
        in each tuple is the coded value for the option
        that will appear in the URL query. The second value
        is the human-readable name for the option that will
        appear in the right side bar"""

        return (
            (instr.id, gettext_lazy(str(instr)))
            for instr in Instrument.objects.all()
        )

    def queryset(self, request, queryset):
        """Returns the filtered queryset based on the
        value provided in the query string and retrievable
        via `self.value()`"""

        return (
            queryset if self.value() is None
            else queryset.filter(instrument__id=self.value())
        )


class SlotAdmin(admin.ModelAdmin):
    change_list_template = "admin/slot_change_list.html"
    list_filter = (
        ('date', DateRangeFilter),
        'status',
        SlotFilterByInstrument
    )
    list_display = admin.ModelAdmin.list_display + ('status',)

    # 'Add Slot' button is only visible to the admin
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def time_left(self, current, end, duration):
        """Checks if a slot can be made with `current time` and
        `duration` before the `end time`"""
        today = datetime.date.today()
        diff = (datetime.datetime.combine(today, end) -
                datetime.datetime.combine(today, current))

        return (diff >= duration)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("bulk-slots/", self.generate_slots),
        ]
        return my_urls + urls

    def render_bulk_slots_form(self, request, form):
        payload = {"form": form}
        return render(request, "admin/bulk_import_slots_form.html", payload)

    def generate_slots(self, request):
        """Bulk Import Slots has a form for creating slots.
        This form is restricted to staff.
        """
        # TODO: Check time slot overlap

        INTERVAL_CHOICES = {
            "1-hour": datetime.timedelta(hours=1),
            "2-hour": datetime.timedelta(hours=2),
            "3-hour": datetime.timedelta(hours=3),
            "4-hour": datetime.timedelta(hours=4),
            "6-hour": datetime.timedelta(hours=6),
            "8-hour": datetime.timedelta(hours=8),
        }

        if request.method == 'POST':
            form = BulkTimeSlotForm(request.POST)
            if not form.is_valid():
                messages.error(request, "Invalid form data!")
                return self.render_bulk_slots_form(request, form)

            instr = form.cleaned_data['instruments']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            duration = form.cleaned_data['slot_duration']
            # number of days for which the timeslot has to be made
            delta = int(form.cleaned_data['for_the_next'])

            # handle exceptional cases
            if start_time >= end_time:
                messages.error(request, "Start time cannot be greater than end time!")
                return self.render_bulk_slots_form(request, form)
            elif start_date < datetime.date.today():
                messages.error(request, "Start date cannot be before today")
                return self.render_bulk_slots_form(request, form)

            # Check if we can make a whole number of slots between start and end time
            combined_start_time = datetime.datetime.combine(start_date, start_time)
            combined_end_time = datetime.datetime.combine(start_date, end_time)
            if not float.is_integer((combined_end_time - combined_start_time) / duration):
                messages.error(request, "Cannot create whole number of slots between "
                                        "specified start and end time with the given duration")
                return self.render_bulk_slots_form(request, form)

            # get the next `delta` days after `today`
            next_days = [start_date + datetime.timedelta(days=var) for var in range(0, delta)]
            # remove the sundays, these two lines can be merged using the walrus op
            next_days = [day for day in next_days if not day.weekday() == 6]

            if not next_days:
                messages.error(request, "The list of days to create slots is empty! Note that slots that fall on "
                                        "Sunday are removed.")
                return self.render_bulk_slots_form(request, form)


            # generate datetime objects for the next `delta` days
            all_slots = {}
            for day in next_days:
                day_wise = []
                current = datetime.datetime.combine(day, start_time)
                end = datetime.datetime.combine(day, end_time)
                while current < end:
                    day_wise.append(current.time())
                    current = current + duration
                all_slots[day] = day_wise

            total_slots, slots_created = 0, 0
            for day, time_slots in all_slots.items():
                for slot_begin in time_slots:
                    slot_end = (datetime.datetime.combine(day, slot_begin) +
                                duration).time()
                    total_slots += 1

                    # Check if an existing slot overlaps with new one
                    big_q = (
                        Q(
                            # Completely inside existing slot
                            start_time__lte=slot_begin,
                            end_time__gte=slot_end,
                        ) |
                        Q(
                            # Begins before existing slot ends
                            end_time__gt=slot_begin,
                            end_time__lt=slot_end,
                        ) |
                        Q(
                            # Ends after existing slot begins
                            start_time__gt=slot_begin,
                            start_time__lt=slot_end,
                        ) |
                        Q(
                            # Subsume existing slot
                            start_time__gte=slot_begin,
                            end_time__lte=slot_end,
                        )
                    )

                    if not Slot.objects.filter(big_q, instrument=instr, date=day).exists():
                        slot_obj = Slot(
                            instrument=instr,
                            status=Slot.STATUS_1,
                            date=day,
                            start_time=slot_begin,
                            end_time=slot_end,
                        )
                        slot_obj.save()
                        slots_created += 1

            if total_slots == slots_created:
                messages.success(request, "All slots were created successfully.")
            else:
                messages.warning(request, "Some slots were not created due to clashes with existing slots.")
            return redirect("..")
        else:
            form = BulkTimeSlotForm()
            return self.render_bulk_slots_form(request, form)
