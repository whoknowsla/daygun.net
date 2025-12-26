from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'language', 'is_active', 'created_at']
    list_filter = ['language', 'is_active', 'created_at']
    search_fields = ['email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} subscriber(s) activated.')
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} subscriber(s) deactivated.')
    deactivate_subscribers.short_description = "Deactivate selected subscribers"
