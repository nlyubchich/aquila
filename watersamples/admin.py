from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from watersamples.models import OrganizationInfo, Laboratory, WaterIntakeInfo, WaterIntakePoint

admin.site.register([Laboratory, WaterIntakePoint])


class EmployeeInline(admin.StackedInline):
    model = OrganizationInfo
    can_delete = False
    verbose_name_plural = 'OrganizationInfos'


class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]


class WaterIntakeInfoAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        # obj is not None, so this is an edit
        addition_fields = ['classification', 'classification_reason_field']
        if obj:
            # Return a list or tuple of readonly fields' names
            return addition_fields + ['temperature', 'user', 'intake_point']
        else:  # This is an addition
            return addition_fields

admin.site.register(WaterIntakeInfo, WaterIntakeInfoAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
