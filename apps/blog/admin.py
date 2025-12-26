from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'slug', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'created_at', 'published_at']
    search_fields = ['title_en', 'title_tr', 'slug', 'content_en', 'content_tr']
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Turkish Content', {
            'fields': ('title_tr', 'summary_tr', 'content_tr')
        }),
        ('English Content', {
            'fields': ('title_en', 'summary_en', 'content_en')
        }),
        ('Metadata', {
            'fields': ('slug', 'is_published', 'published_at', 'newsletter_sent')
        }),
    )
    readonly_fields = ['newsletter_sent']
