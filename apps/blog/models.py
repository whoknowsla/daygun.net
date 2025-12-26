from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import bleach

class BlogPost(models.Model):
    title_tr = models.CharField(max_length=255, verbose_name="Title (Turkish)")
    title_en = models.CharField(max_length=255, verbose_name="Title (English)")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    summary_tr = models.TextField(blank=True, verbose_name="Summary (Turkish)")
    summary_en = models.TextField(blank=True, verbose_name="Summary (English)")
    content_tr = models.TextField(verbose_name="Content (Turkish)")
    content_en = models.TextField(verbose_name="Content (English)")
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    newsletter_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title_en or self.title_tr

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en or self.title_tr)
        
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
            send_newsletter = True
        else:
            send_newsletter = False

        self.content_tr = self.sanitize_markdown(self.content_tr)
        self.content_en = self.sanitize_markdown(self.content_en)
        
        super().save(*args, **kwargs)
        
        if send_newsletter and not self.newsletter_sent:
            from apps.subscriptions.utils import send_new_post_newsletter
            send_new_post_newsletter(self)
            self.newsletter_sent = True
            super().save(update_fields=['newsletter_sent'])

    @staticmethod
    def sanitize_markdown(content):
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 's', 'a', 'ul', 'ol', 'li',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre',
            'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'img'
        ]
        allowed_attrs = {
            'a': ['href', 'title', 'rel'],
            'img': ['src', 'alt', 'title'],
            'code': ['class'],
        }
        return bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    def get_title(self, lang):
        return getattr(self, f'title_{lang}', self.title_en)

    def get_summary(self, lang):
        return getattr(self, f'summary_{lang}', self.summary_en)

    def get_content(self, lang):
        return getattr(self, f'content_{lang}', self.content_en)
