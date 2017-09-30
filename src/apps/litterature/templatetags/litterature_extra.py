from src.apps.authentication.models import User as User
from django import template
from django.conf import settings
from ..models import Book, Read, Recommended

register = template.Library()

@register.simple_tag
def is_read_glyph(user_pk, book_pk):
    user = User.objects.get(pk=user_pk)
    book = Book.objects.get(pk=book_pk)

    if Read.objects.filter(book=book, user=user).exists():
        return "glyphicon-star"
    else:
        return "glyphicon-star-empty"

@register.simple_tag
def is_rec_glyph(user_pk, book_pk):
    user = User.objects.get(pk=user_pk)
    book = Book.objects.get(pk=book_pk)

    if Recommended.objects.filter(book=book, user=user).exists():
        return "glyphicon-ok"
    else:
        return "glyphicon-minus"

@register.simple_tag
def is_read_text(user_pk, book_pk):
    user = User.objects.get(pk=user_pk)
    book = Book.objects.get(pk=book_pk)

    if Read.objects.filter(book=book, user=user).exists():
        return "Lest"
    else:
        return "Ikke lest"

@register.simple_tag
def is_rec_text(user_pk, book_pk):
    user = User.objects.get(pk=user_pk)
    book = Book.objects.get(pk=book_pk)

    if Recommended.objects.filter(book=book, user=user).exists():
        return "Anbefalt"
    else:
        return "Anbefal"


@register.simple_tag
def get_author_list(book_pk):
    book = Book.objects.get(pk=book_pk)
    authors = ""
    print("Authors to book ", book.title, ": ", book.author.all())
    for author in book.author.all():
        authors += author.first_name + " " + author.last_name + ", "
    print("Authors in get_authors_list: ", authors)
    return authors[:-2]


# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")