from django.contrib import admin


class InstrumentAdmin(admin.ModelAdmin):
    list_filter = admin.ModelAdmin.list_filter + ('status',)