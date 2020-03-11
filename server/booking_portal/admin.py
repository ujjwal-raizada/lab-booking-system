from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Student, Faculty, EmailModel, LabAssistant
from .models import Instrument, Slot, Request
from .models import FTIR, FESEM, LCMS, TCSPC, UserDetails

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(EmailModel)
admin.site.register(LabAssistant)
admin.site.register(Instrument)
admin.site.register(Slot)
admin.site.register(Request)
admin.site.register(FTIR)
admin.site.register(FESEM)
admin.site.register(LCMS)
admin.site.register(TCSPC)
admin.site.register(UserDetails)