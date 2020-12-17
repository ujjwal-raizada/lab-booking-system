from .user import CustomUserAdmin
from ... import forms


class StudentAdmin(CustomUserAdmin):
    form = forms.StudentChangeForm
    add_form = forms.StudentCreationForm

    list_filter = CustomUserAdmin.list_filter + ('supervisor', )
    list_display = CustomUserAdmin.list_display + ('supervisor',)
    fieldsets = CustomUserAdmin.fieldsets + (
        (None, {'fields' : ('supervisor',)},),
    )
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        (None, {
            'classes' : ('wide',),
            'fields' : ('supervisor',)}
        ),
    )
