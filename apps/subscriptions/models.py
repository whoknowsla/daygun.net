from django.db import models

class Subscriber(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('tr', 'Turkish'),
    ]
    
    email = models.EmailField(unique=True, db_index=True, verbose_name="Email")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en', verbose_name="Language")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return f"{self.email} ({self.language})"

    @classmethod
    def subscribe(cls, email, language='en'):
        subscriber, created = cls.objects.get_or_create(
            email=email,
            defaults={'language': language, 'is_active': True}
        )
        
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.language = language
            subscriber.save()
        
        return subscriber, created
