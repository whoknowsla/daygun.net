from django.db import models
import bleach

class Project(models.Model):
    title_tr = models.CharField(max_length=255, verbose_name="Title (Turkish)")
    title_en = models.CharField(max_length=255, verbose_name="Title (English)")
    short_description_tr = models.TextField(verbose_name="Short Description (Turkish)")
    short_description_en = models.TextField(verbose_name="Short Description (English)")
    description_tr = models.TextField(verbose_name="Description (Turkish)")
    description_en = models.TextField(verbose_name="Description (English)")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    live_url = models.URLField(blank=True, verbose_name="Live URL")
    is_featured = models.BooleanField(default=False, verbose_name="Featured")
    order = models.IntegerField(default=0, verbose_name="Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title_en or self.title_tr

    def save(self, *args, **kwargs):
        self.description_tr = self.sanitize_markdown(self.description_tr)
        self.description_en = self.sanitize_markdown(self.description_en)
        super().save(*args, **kwargs)

    @staticmethod
    def sanitize_markdown(content):
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 's', 'a', 'ul', 'ol', 'li',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre',
            'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td'
        ]
        allowed_attrs = {
            'a': ['href', 'title', 'rel'],
            'code': ['class'],
        }
        return bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    def get_title(self, lang):
        return getattr(self, f'title_{lang}', self.title_en)

    def get_short_description(self, lang):
        return getattr(self, f'short_description_{lang}', self.short_description_en)

    def get_description(self, lang):
        return getattr(self, f'description_{lang}', self.description_en)


class Experience(models.Model):
    title_tr = models.CharField(max_length=255, verbose_name="Title (Turkish)")
    title_en = models.CharField(max_length=255, verbose_name="Title (English)")
    company_tr = models.CharField(max_length=255, verbose_name="Company (Turkish)")
    company_en = models.CharField(max_length=255, verbose_name="Company (English)")
    description_tr = models.TextField(verbose_name="Description (Turkish)")
    description_en = models.TextField(verbose_name="Description (English)")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    is_current = models.BooleanField(default=False, verbose_name="Current Position")
    order = models.IntegerField(default=0, verbose_name="Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return f"{self.title_en} at {self.company_en}"

    def get_title(self, lang):
        return getattr(self, f'title_{lang}', self.title_en)

    def get_company(self, lang):
        return getattr(self, f'company_{lang}', self.company_en)

    def get_description(self, lang):
        return getattr(self, f'description_{lang}', self.description_en)


class AboutContent(models.Model):
    bio_short_tr = models.TextField(verbose_name="Short Bio (Turkish)")
    bio_short_en = models.TextField(verbose_name="Short Bio (English)")
    bio_full_tr = models.TextField(verbose_name="Full Bio (Turkish)")
    bio_full_en = models.TextField(verbose_name="Full Bio (English)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Content"
        verbose_name_plural = "About Content"

    def __str__(self):
        return "About Page Content"

    def get_bio_short(self, lang):
        return getattr(self, f'bio_short_{lang}', self.bio_short_en)

    def get_bio_full(self, lang):
        return getattr(self, f'bio_full_{lang}', self.bio_full_en)
