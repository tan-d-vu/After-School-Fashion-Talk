"""after_school_fashion_talk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from asft_core import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('accounts/', include('allauth.urls')),
    path('accounts/<username>/update', views.profile_update, name='update'),

    path('message/send/<username>/', views.MessageCreateView.as_view(), name='send_message'),
    path('message/<username>/inbox/', views.InboxView.as_view(), name='inbox'),
    path('message/<username>/sent/', views.SentMessageView.as_view(), name='sent_messages'),
    path('<username>/friends/suggestions/', views.friend_suggestions_view, name='friend_suggestions'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
