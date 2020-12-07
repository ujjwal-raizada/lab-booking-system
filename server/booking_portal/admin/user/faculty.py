from ... import forms
from .user import CustomUserAdmin

class FacultyAdmin(CustomUserAdmin):
    form = forms.FacultyChangeForm
    add_form = forms.FacultyCreationForm

    list_display = CustomUserAdmin.list_display + ('department',)
    fieldsets = CustomUserAdmin.fieldsets + (
        (None, {'fields' : ('department',)},),
    )
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        (None, {
            'classes' : ('wide',),
            'fields' : ('department',)}
        ),
    )