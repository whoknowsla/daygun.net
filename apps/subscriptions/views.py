from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Subscriber
from .forms import SubscriberForm

def subscribe(request, lang_code):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = Subscriber.subscribe(email, lang_code)
            
            if created:
                msg = "Successfully subscribed!" if lang_code == 'en' else "Başarıyla abone oldunuz!"
            else:
                msg = "You're already subscribed!" if lang_code == 'en' else "Zaten abone oldunuz!"
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': msg})
            
            messages.success(request, msg)
            return redirect(request.META.get('HTTP_REFERER', f'/{lang_code}/'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            
            messages.error(request, 'Invalid email address.' if lang_code == 'en' else 'Geçersiz e-posta adresi.')
            return redirect(request.META.get('HTTP_REFERER', f'/{lang_code}/'))
    
    return redirect(f'/{lang_code}/')

def unsubscribe(request, lang_code):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.is_active = False
            subscriber.save()
            
            msg = "Successfully unsubscribed." if lang_code == 'en' else "Abonelikten çıkıldı."
            messages.success(request, msg)
        except Subscriber.DoesNotExist:
            msg = "Email not found." if lang_code == 'en' else "E-posta bulunamadı."
            messages.error(request, msg)
    
    return redirect(f'/{lang_code}/')
