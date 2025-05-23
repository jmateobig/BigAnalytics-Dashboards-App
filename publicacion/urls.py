"""
URL configuration for publicacion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from dashboard.views import IndexView
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),
    path('', include('pwa.urls')),
    path('', IndexView.as_view(), name='index'),

    path('user/',include('user.urls_user')),
    path('category/',include('category.urls')),
    path('group/',include('user.urls_group')),
    path('dashboard/',include('dashboard.urls')),
    path('notification/',include('notification.urls')),
]

def custom_403(request, exception):
    return render(request, 'errors/403.html', status=403)
handler403 = custom_403