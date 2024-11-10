from django.contrib import admin
from .models import Product, TrackingStatus, Notification, BitcoinWallet, BitcoinPayment

admin.site.register(BitcoinWallet)
admin.site.register(BitcoinPayment)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'sender_name', 'recipient_name', 'current_status', 'created_at')
    list_filter = ('current_status', 'created_at')
    search_fields = ('tracking_number', 'sender_name', 'recipient_name')
    readonly_fields = ('tracking_number',)

@admin.register(TrackingStatus)
class TrackingStatusAdmin(admin.ModelAdmin):
    list_display = ('product', 'status', 'location', 'latitude', 'longitude', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('product__tracking_number', 'location')
    fieldsets = (
        (None, {
            'fields': ('product', 'status', 'location', 'description')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')