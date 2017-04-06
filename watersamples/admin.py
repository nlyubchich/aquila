from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import TextInput, Media
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from watersamples.models import OrganizationInfo, Laboratory, WaterIntakeInfo, WaterIntakePoint

admin.site.register(Laboratory)


class EmployeeInline(admin.StackedInline):
    model = OrganizationInfo
    can_delete = False
    verbose_name_plural = 'OrganizationInfos'


class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]


class WaterIntakeInfoAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        # obj is not None, so this is an edit
        addition_fields = ['classification', 'classification_reason_field', 'status']
        if obj:
            # Return a list or tuple of readonly fields' names
            return addition_fields + ['temperature', 'user', 'intake_point']
        else:  # This is an addition
            return addition_fields


admin.site.register(WaterIntakeInfo, WaterIntakeInfoAdmin)


class CustomGoogleMapsAddressWidget(map_widgets.GoogleMapsAddressWidget):
    media = Media(
        js=(
            'https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js',
            'https://maps.google.com/maps/api/js?key={}'.format(
                settings.GOOGLE_MAPS_API_KEY
            ),
            settings.STATIC_URL + 'django_google_maps/js/google-maps-admin.js',
        ),
    )

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        html = u'<input%s /><div class="map_canvas_wrapper"><div id="map_canvas" style="width: 100%%; height: 40em"></div></div>'
        return mark_safe(html % flatatt(final_attrs))


class WaterIntakePointAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': CustomGoogleMapsAddressWidget},
        map_fields.GeoLocationField: {'widget': TextInput(attrs={'readonly': 'readonly'})},
    }


admin.site.register(WaterIntakePoint, WaterIntakePointAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
