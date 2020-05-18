"""MSHD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
import front.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url

urlpatterns = [

    url(r'^$', front.views.index),
    url(r'^test_url/', front.views.test_url),
    path('upload_file/', front.views.upload_file),
    # url(r'^upload_file/commDisater.json', front.views.upload_file),
    url(r'^data/*', front.views.data, name='data'),
    url(r'^request/', front.views.data_request),
    # path('status.html/',front.views.status),
    url(r'^status/*',front.views.status, name='status'),
]

urlpatterns += staticfiles_urlpatterns()
