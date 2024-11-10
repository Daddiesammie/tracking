from django.contrib import admin
from .models import ChatScript

@admin.register(ChatScript)
class ChatScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'script_tag']
    readonly_fields = ['created_at', 'updated_at']
