# -*- encoding: utf-8 -*-

from django.conf.urls import url

from src.apps.profile import views

urlpatterns = [
    # TODO: pk is showing after profile/ - delete?
    url(r'^(?P<pk>[0-9]+)/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.EditUserProfileView.as_view(), name='edit_profile'),
    url(r'^members$', views.MembersListView.as_view(), name='members_list')

]