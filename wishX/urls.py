"""Wishx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
# if you have multilang website uncomment
from django.conf.urls.static import static
from core.consumers import *
from django.conf.urls.i18n import i18n_patterns  # for url translation

# from oscar.app import application # oscar applications urls here


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('labmin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

websocket_urlpatterns = [
    path('comment/<slug:slug>', CommentConsumer, name='donation-comment'),
    path('like/<slug:slug>', LikeDislikeConsumer, name='like-dislike'),
]

urlpatterns += i18n_patterns(
    path('', include("core.urls", namespace='core')),
    path('page/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('base_user.urls', namespace='account')),
)

urlpatterns += websocket_urlpatterns

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('translation/', include('rosetta.urls'))
    ]

# handler404 = 'game.views.NotFoundPage.as_view'

# in development django built-in server serves static and media content
if not settings.PROD:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# This is change default admin panel Headers and titles
admin.site.site_header = 'Wishx Admin'
admin.site.site_title = 'Wishx Administration'
admin.site.index_title = 'Wishx Administration'
