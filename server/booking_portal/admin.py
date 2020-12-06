import csv
import datetime
from io import TextIOWrapper

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import path
from django.core.exceptions import MultipleObjectsReturned
from django.contrib import admin, messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from .models import CustomUser, Student, Faculty, EmailModel, LabAssistant, Slot, Instrument
from .models import Instrument, Slot, Request
from .models import FTIR, FESEM, LCMS, TCSPC, UserDetails
from .models import Rheometer, AAS, TGA, BET, CDSpectrophotometer
from .models import LSCM, DSC, GC, EDXRF, HPLC, NMR
from .models import PXRD, SCXRD, XPS, UVSpectrophotometer
from .forms.adminForms import BulkImportForm
from .forms.adminForms import BulkImportForm, BulkTimeSlotForm


CSV_HEADERS = ('username', 'password')
CSV_HEADERS_STUDENT = CSV_HEADERS + ('supervisor',)
CSV_HEADERS_FACULTY = CSV_HEADERS + ('department', )

def create_users(user_type, records):
    headers = CSV_HEADERS
    if user_type == Student:
        headers = CSV_HEADERS_STUDENT
    elif user_type == Faculty:
        headers = CSV_HEADERS_FACULTY

    if set(records.fieldnames) != set(headers):
        raise Exception(f"Invalid CSV headers/columns. Expected: {headers}")

    for record in records:
        record['password'] = make_password(record['password'])
        if user_type == Student:
            obj = Faculty.objects.filter(username=record['supervisor']).first()
            if not obj:
                raise Exception(f"Invalid Supervisor Name: \"{record['supervisor']}\"")
            else:
                record['supervisor'] = obj

        if user_type.objects.filter(username=record['username']).first():
            raise Exception(f"{user_type} with username \"{record['username']}\" already exists.")
        else:
            user_type.objects.create(**record)


def time_left(current, end, duration):
    today = datetime.date.today()
    diff = (datetime.datetime.combine(today, end) -
            datetime.datetime.combine(today, current))

    return (diff >= duration)

class BulkImportAdmin(UserAdmin):
    change_list_template = "admin/csv_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            try:
                csv_file = TextIOWrapper(
                    request.FILES['csv_file'].file,
                    encoding=request.encoding
                )
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                csv_file.seek(0)
                reader = csv.DictReader(csv_file, dialect=dialect)
            except Exception as err:
                self.message_user(request, "Error: {}".format(err))
                return redirect("..")
            try:
                if '/student/' in request.path:
                    user_type = Student
                elif '/faculty/' in request.path:
                    user_type = Faculty
                elif '/labassistant/' in request.path:
                    user_type = LabAssistant
                else:
                    raise Http404
                create_users(user_type, reader)
            except Exception as err:
                messages.error(request, f'Error on row number {reader.line_num}: {err}')
            else:
                messages.success(request, "Your csv file has been imported")
            return redirect("..")
        form = BulkImportForm()
        payload = {"form": form}
        return render(
            request, "admin/bulk_import_form.html", payload
        )


class BulkSlotImportAdmin(admin.ModelAdmin):
    change_list_template = "admin/slot_change_list.html"

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
                while current < end and time_left(current, end, duration) == True:
                    day_wise.append(datetime.datetime.combine(day, current))
                    current = datetime.time(hour=(datetime.datetime.combine(day, current) + duration).hour)
                all_slots[day] = day_wise

            for day, time_slots in all_slots.items():
                for time_slot in time_slots:
                    if not Slot.objects.filter(date=day, time=time_slot.time()).exists():
                        slot_obj = Slot(slot_name=instr.name, instrument=instr,
                                        status=Slot.STATUS_1, date=day, time=time_slot.time())
                        slot_obj.save()

            return redirect("..")
        form = BulkTimeSlotForm()
        payload = {"form": form}
        return render(
            request, "admin/bulk_import_slots_form.html", payload
        )

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('supervisor',)

class StudentChangeForm(UserChangeForm):
    class Meta:
        model = Student
        fields = ('supervisor',)

class StudentAdmin(BulkImportAdmin):
    form = StudentChangeForm
    add_form = StudentCreationForm

    list_display = UserAdmin.list_display + ('supervisor',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields' : ('supervisor',)},),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes' : ('wide',),
            'fields' : ('supervisor',)}
        ),
    )

class FacultyCreationForm(UserCreationForm):
    class Meta:
        model = Faculty
        fields = ('department',)

class FacultyChangeForm(UserChangeForm):
    class Meta:
        model = Faculty
        fields = ('department',)

class FacultyAdmin(BulkImportAdmin):
    form = FacultyChangeForm
    add_form = FacultyCreationForm

    list_display = UserAdmin.list_display + ('department',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields' : ('department',)},),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes' : ('wide',),
            'fields' : ('department',)}
        ),
    )

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(EmailModel)
admin.site.register(LabAssistant, BulkImportAdmin)
admin.site.register(Instrument)
admin.site.register(Request)
admin.site.register(FTIR)
admin.site.register(FESEM)
admin.site.register(LCMS)
admin.site.register(TCSPC)
admin.site.register(UserDetails)
admin.site.register(Rheometer)
admin.site.register(AAS)
admin.site.register(TGA)
admin.site.register(BET)
admin.site.register(CDSpectrophotometer)
admin.site.register(LSCM)
admin.site.register(DSC)
admin.site.register(GC)
admin.site.register(EDXRF)
admin.site.register(HPLC)
admin.site.register(NMR)
admin.site.register(PXRD)
admin.site.register(SCXRD)
admin.site.register(XPS)
admin.site.register(UVSpectrophotometer)
admin.site.register(Slot, BulkSlotImportAdmin)
