# -*- encoding: utf-8 -*-

from django.conf.urls import url

from src.apps.forum import views

urlpatterns = [
    url(r'^$', views.ForumListView.as_view(), name='forum'),
    url(r'^(?P<pk>[^\.]+)/', views.ForumPostDetailView.as_view(), name='forum_post'),
    url(r'^create', views.CreatePostFormView.as_view(), name='create_post'),
]

