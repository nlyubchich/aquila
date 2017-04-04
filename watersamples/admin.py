from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from watersamples.models import OrganizationInfo, Laboratory, WaterIntakeInfo, WaterIntakePoint

admin.site.register([Laboratory, WaterIntakeInfo, WaterIntakePoint])


class EmployeeInline(admin.StackedInline):
    model = OrganizationInfo
    can_delete = False
    verbose_name_plural = 'OrganizationInfos'


class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
