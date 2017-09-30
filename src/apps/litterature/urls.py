# -*- encoding: utf-8 -*-

from django.conf.urls import url

from src.apps.litterature import views

urlpatterns = [
    url(r'^$', views.LitteratureListView.as_view(), name="book_list"),
    url(r'^(?P<pk>[^\.]+)/', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^add', views.AddBookView.as_view(), name='add_book'),
]