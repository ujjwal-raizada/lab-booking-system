from django.contrib import admin
from ..forms import InstrumentCreateForm, InstrumentChangeForm


class InstrumentAdmin(admin.ModelAdmin):
    form = InstrumentChangeForm
    add_form = InstrumentCreateForm

    list_filter = admin.ModelAdmin.list_filter + ('status',)