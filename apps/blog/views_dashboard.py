from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost
from .forms import BlogPostForm

@login_required
def dashboard_post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/dashboard/list.html', {'posts': posts})

@login_required
def dashboard_post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('dashboard_post_edit', post_id=post.id)
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/dashboard/form.html', {'form': form, 'action': 'Create'})

@login_required
def dashboard_post_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('dashboard_post_edit', post_id=post.id)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/dashboard/form.html', {
        'form': form,
        'post': post,
        'action': 'Edit'
    })

@login_required
def dashboard_post_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('dashboard_post_list')
    
    return render(request, 'blog/dashboard/delete.html', {'post': post})
