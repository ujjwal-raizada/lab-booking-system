import datetime

from django.contrib import admin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.translation import gettext_lazy
from rangefilter.filter import DateRangeFilter

from ..forms.adminForms import BulkCreateSlotsForm
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
            form = BulkCreateSlotsForm(request.POST)
            if not form.is_valid():
                return self.render_bulk_slots_form(request, form)

            instr = form.cleaned_data['instrument']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            duration = form.cleaned_data['slot_duration']
            day_count = int(form.cleaned_data['for_the_next'])

            total, created = Slot.objects.bulk_create_slots(instr, start_date, start_time, end_time, duration, day_count)

            if total == created:
                messages.success(request, "All slots were created successfully.")
            else:
                messages.warning(request, "Some slots were not created due to clashes with existing slots.")
            return redirect("..")
        else:
            form = BulkCreateSlotsForm()
            return self.render_bulk_slots_form(request, form)
