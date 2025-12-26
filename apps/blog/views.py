from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost

def blog_list(request, lang_code):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    posts = BlogPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Set language-specific getters for each post
    for post in page_obj:
        post.get_title = lambda p=post: p.get_title(lang_code)
        post.get_summary = lambda p=post: p.get_summary(lang_code)
    
    return render(request, 'blog/list.html', {
        'page_obj': page_obj,
        'lang_code': lang_code
    })

def blog_detail(request, lang_code, slug):
    if lang_code not in ['en', 'tr']:
        lang_code = 'en'
    
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Set title and content based on language
    post.get_title = lambda: post.get_title(lang_code)
    post.get_summary = lambda: post.get_summary(lang_code)
    post.get_content = lambda: post.get_content(lang_code)
    
    return render(request, 'blog/detail.html', {
        'post': post,
        'lang_code': lang_code
    })
