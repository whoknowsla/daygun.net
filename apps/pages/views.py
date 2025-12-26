from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from apps.blog.models import BlogPost
from .models import Project, Experience, AboutContent, Social, ContactInfo

def home_redirect(request):
    lang = request.GET.get('lang', '')
    
    if not lang:
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        if 'tr' in accept_language.lower():
            lang = 'tr'
        else:
            lang = 'en'
    
    return redirect(f'/{lang}/')

def home(request, lang_code):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    about_content = AboutContent.objects.first()
    if about_content:
        about_content.get_bio_short = lambda: about_content.get_bio_short(lang_code)
    
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]
    for post in recent_posts:
        post.get_title = lambda p=post: p.get_title(lang_code)
        post.get_summary = lambda p=post: p.get_summary(lang_code)
    
    return render(request, 'pages/home.html', {
        'about_content': about_content,
        'recent_posts': recent_posts,
        'lang_code': lang_code
    })

def about(request, lang_code):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    about_content = AboutContent.objects.first()
    if about_content:
        about_content.get_bio_full = lambda: about_content.get_bio_full(lang_code)
    
    experiences = Experience.objects.all()
    for exp in experiences:
        exp.get_title = lambda e=exp: e.get_title(lang_code)
        exp.get_company = lambda e=exp: e.get_company(lang_code)
        exp.get_description = lambda e=exp: e.get_description(lang_code)
    
    return render(request, 'pages/about.html', {
        'about_content': about_content,
        'experiences': experiences,
        'lang_code': lang_code
    })

def projects(request, lang_code):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    all_projects = Project.objects.all()
    for proj in all_projects:
        proj.get_title = lambda p=proj: p.get_title(lang_code)
        proj.get_short_description = lambda p=proj: p.get_short_description(lang_code)
        proj.get_description = lambda p=proj: p.get_description(lang_code)
    
    return render(request, 'pages/projects.html', {
        'projects': all_projects,
        'lang_code': lang_code
    })

def contact(request, lang_code):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    contact_info = ContactInfo.objects.first()
    if contact_info:
        contact_info.get_location = lambda: contact_info.get_location(lang_code)
        contact_info.get_contact_text = lambda: contact_info.get_contact_text(lang_code)
    
    socials = Social.objects.filter(is_active=True)
    
    return render(request, 'pages/contact.html', {
        'contact_info': contact_info,
        'socials': socials,
        'lang_code': lang_code
    })
