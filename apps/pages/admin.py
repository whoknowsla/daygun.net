from django.contrib import admin
from .models import Project, Experience, AboutContent, Social, ContactInfo

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured']
    search_fields = ['title_en', 'title_tr', 'description_en', 'description_tr']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Turkish Content', {
            'fields': ('title_tr', 'short_description_tr', 'description_tr')
        }),
        ('English Content', {
            'fields': ('title_en', 'short_description_en', 'description_en')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Settings', {
            'fields': ('is_featured', 'order')
        }),
    )

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'company_en', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['title_en', 'title_tr', 'company_en', 'company_tr']
    ordering = ['-start_date', 'order']
    
    fieldsets = (
        ('Turkish Content', {
            'fields': ('title_tr', 'company_tr', 'description_tr')
        }),
        ('English Content', {
            'fields': ('title_en', 'company_en', 'description_en')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Settings', {
            'fields': ('order',)
        }),
    )

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated_at']
    
    fieldsets = (
        ('Turkish Content', {
            'fields': ('bio_short_tr', 'bio_full_tr')
        }),
        ('English Content', {
            'fields': ('bio_short_en', 'bio_full_en')
        }),
    )
    
    def has_add_permission(self, request):
        return not AboutContent.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ['platform', 'username', 'url', 'is_active', 'order']
    list_filter = ['platform', 'is_active']
    search_fields = ['username', 'url']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('platform', 'username', 'url', 'is_active', 'order')
        }),
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'updated_at']
    
    fieldsets = (
        ('Contact Details', {
            'fields': ('email', 'phone')
        }),
        ('Turkish Content', {
            'fields': ('location_tr', 'contact_text_tr')
        }),
        ('English Content', {
            'fields': ('location_en', 'contact_text_en')
        }),
    )
    
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
