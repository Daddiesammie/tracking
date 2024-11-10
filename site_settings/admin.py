from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('site_name', 'logo', 'favicon', 'email', 'phone', 'address')
        }),
        ('Social Links', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Content', {
            'fields': ('about_us', 'terms_and_conditions', 'privacy_policy', 'disclaimer')
        }),
        ('Advanced', {
            'fields': ('maintenance_mode', 'google_analytics_id', 'custom_css', 'custom_js'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only superusers can add settings and only if no settings exist
        return request.user.is_superuser and not SiteSettings.objects.exists()

    def has_change_permission(self, request, obj=None):
        # Only superusers can modify settings
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete settings
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        # Staff members can view settings
        return request.user.is_staff
