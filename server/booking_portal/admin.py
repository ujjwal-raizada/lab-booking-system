from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Student, Faculty, EmailModel, LabAssistant


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(EmailModel)
admin.site.register(LabAssistant)


