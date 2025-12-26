from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title_tr', 'title_en', 'slug', 'summary_tr', 'summary_en', 
                  'content_tr', 'content_en', 'is_published']
        widgets = {
            'title_tr': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Turkish title'
            }),
            'title_en': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'English title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'url-slug'
            }),
            'summary_tr': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Turkish summary (optional)'
            }),
            'summary_en': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'English summary (optional)'
            }),
            'content_tr': forms.Textarea(attrs={
                'class': 'editor-content',
                'id': 'editor-tr',
                'aria-label': 'Turkish content editor'
            }),
            'content_en': forms.Textarea(attrs={
                'class': 'editor-content',
                'id': 'editor-en',
                'aria-label': 'English content editor'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            })
        }
