from django.contrib import admin
from django.utils.html import format_html
from .models import PricingPlan, Product, TrackingStatus, Notification, BitcoinWallet, BitcoinPayment

class BitcoinPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'payment_proof_preview', 'created_at')  # Removed is_verified
    list_filter = ('created_at',)  # Removed is_verified
    search_fields = ('user__username', 'product__tracking_number')
    readonly_fields = ('payment_proof_preview',)

    def payment_proof_preview(self, obj):
        if obj.payment_proof:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="100" /></a>', 
                             obj.payment_proof.url, obj.payment_proof.url)
        return "No image"
    
    payment_proof_preview.short_description = 'Payment Proof'

# Register models
admin.site.register(BitcoinPayment, BitcoinPaymentAdmin)
admin.site.register(BitcoinWallet)
admin.site.register(PricingPlan)

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
