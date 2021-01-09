from django.contrib import admin

class EmailAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        ## Emails are internally generated
        ## Admins/staff cannot create and send an email object
        return False

    def has_change_permission(self, request, obj=None):
        ## Once an email is sent, it cannot be changed by
        ## admin/staff
        return False
