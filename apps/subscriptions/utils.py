from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Subscriber

def send_new_post_newsletter(post):
    subscribers = Subscriber.objects.filter(is_active=True)
    
    for subscriber in subscribers:
        lang = subscriber.language
        
        subject = post.get_title(lang)
        
        context = {
            'post': post,
            'lang_code': lang,
            'site_url': settings.SITE_URL,
            'unsubscribe_url': f"{settings.SITE_URL}/{lang}/subscribe/unsubscribe/",
            'subscriber_email': subscriber.email
        }
        
        try:
            html_message = render_to_string(f'subscriptions/email_new_post_{lang}.html', context)
            text_message = render_to_string(f'subscriptions/email_new_post_{lang}.txt', context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to {subscriber.email}: {e}")
            continue
