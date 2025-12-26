from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from apps.pages.views import home_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home_redirect'),
    path('i18n/setlang/', set_language, name='set_language'),
    path('dashboard/', include('apps.blog.urls_dashboard')),
    path('<str:lang_code>/', include([
        path('', include('apps.pages.urls')),
        path('blog/', include('apps.blog.urls')),
        path('subscribe/', include('apps.subscriptions.urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
