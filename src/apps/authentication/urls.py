# -*- encoding: utf-8 -*-

from django.conf.urls import url

from src.apps.authentication import views

urlpatterns = [

    url(r'^register/$', views.register, name='auth_register'),
    url(r'^login/$', views.login, name='auth_login'),
    url(r'^logout/$', views.logout, name='auth_logout'),
]