from django.contrib import admin
from django.db import models

from .models import Book, Author, Topic, Review


# Register your models here.

class AuthorAdmin(models.Model):
    """
    fieldset = [
        (None, {'fields': ('first_name', 'last_name')}),
    ]
    """
    fields = ['first_name', 'last_name', 'books']

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Topic)
admin.site.register(Review)
