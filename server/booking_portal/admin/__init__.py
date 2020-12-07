from django.contrib import admin

from .slot import SlotAdmin
from .user import (
        StudentAdmin,
        FacultyAdmin,
        CustomUserAdmin,
)
from ..models import (
                CustomUser, Student, Faculty,
                EmailModel, LabAssistant, Instrument,
                Request, Slot, UserDetail,
)


# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(EmailModel)
admin.site.register(LabAssistant, CustomUserAdmin)
admin.site.register(UserDetail)
admin.site.register(Instrument)
admin.site.register(Request)
admin.site.register(Slot, SlotAdmin)
# admin.site.register(FTIR)
# admin.site.register(FESEM)
# admin.site.register(LCMS)
# admin.site.register(TCSPC)
# admin.site.register(Rheometer)
# admin.site.register(AAS)
# admin.site.register(TGA)
# admin.site.register(BET)
# admin.site.register(CDSpectrophotometer)
# admin.site.register(LSCM)
# admin.site.register(DSC)
# admin.site.register(GC)
# admin.site.register(EDXRF)
# admin.site.register(HPLC)
# admin.site.register(NMR)
# admin.site.register(PXRD)
# admin.site.register(SCXRD)
# admin.site.register(XPS)
# admin.site.register(UVSpectrophotometer)
