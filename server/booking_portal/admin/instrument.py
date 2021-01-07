from django.contrib import admin
from ..forms import InstrumentCreateForm, InstrumentChangeForm


class InstrumentAdmin(admin.ModelAdmin):
    form = InstrumentChangeForm
    add_form = InstrumentCreateForm

    list_filter = admin.ModelAdmin.list_filter + ('status',)

    # only superuser has permission to add instruments
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False
