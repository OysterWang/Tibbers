"""Tibbers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf2
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
#引用static新加入
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#http://localhost:8000/ajax_returnPoint?ip_des=1.1.1.1
urlpatterns = [
    url(r'^trace$', 'apps.trace.views.index', name='trace'), 
    url(r'^ajax_returnPoint/$', 'apps.trace.views.ajax_returnPoint', name='ajax_returnPoint'),
    url(r'^alive','apps.alive.views.index',name='alive'),
    url(r'^admin/', include(admin.site.urls)),  
    url(r'^test', 'apps.trace.views.test')
]

#引用static新加
urlpatterns += staticfiles_urlpatterns()