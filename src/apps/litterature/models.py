# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode

from src.apps.authentication.models import User as User

RATING_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]
class Book(models.Model):

    title = models.CharField("tittel", max_length=100,  blank=False, null=True)
    # Author and Topic is in '' because they are not yet defined
    author = models.ManyToManyField('Author', related_name="book", blank=False)
    topic = models.ManyToManyField('Topic', related_name="+", blank=False)
    published = models.IntegerField("publisert", null=True)
    isbn = models.CharField("isbn", max_length=14, unique=True, blank=False, null=True)
    rating = models.IntegerField('rating', null=True)
    cover_url = models.CharField(null=True, max_length=100)

    selfdefined_tags = models.ManyToManyField('SelfdefinedTag', related_name='selfdefined_tag')

    summary = models.TextField("sammendrag", max_length=1000, null=True)
    shop_url = models.TextField("url", null=True)

    def get_authors():
        author_list = ""
        for a in author:
            author_list += a.get_full_name() + ", "
        return author_list.strip[-2]

    @property
    def slug(self):
        # TODO: isbn instead?
        return slugify(unidecode(self.isbn))

    # To show name of object in djangoadmin
    def __str__(self):
        if self.title is None or len(self.title) == 0:
            return "No title on book"
        else:
            return self.title


class Author(models.Model):

    first_name = models.CharField("first_name", max_length=50)
    last_name = models.CharField("last_name", max_length=50)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def slug(self):
        return slugify(unidecode(self.first_name, self.last_name))

    def __str__(self):
        return self.first_name + " " + self.last_name


class Topic(models.Model):

    name = models.CharField("topic", max_length=100)
    belong_to = models.CharField("belongs_to", max_length=20)
    # List of books related to that topic
    books = models.ManyToManyField(Book, related_name="topics", blank=True)

    def slug(self):
        return slugify(unidecode(self.name))

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.CharField("title", max_length = 100, blank=False, null=True)
    author = models.ForeignKey(User, related_name="rev_author", blank=False, null=True)
    published = models.DateField(blank=False, null=True)
    review = models.TextField("review", max_length = 500, blank=False, null=True)
    book = models.ForeignKey(Book, related_name="rev_book", on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField("rating", choices=RATING_CHOICES, blank=False, null=True)

    def __str__(self):
        return self.title


# TODO: makes as a BookUserRel with type?
class Read(models.Model):
    book = models.ForeignKey('Book')
    user = models.ForeignKey('authentication.User')


class Recommended(models.Model):
    book = models.ForeignKey('Book')
    user = models.ForeignKey('authentication.User')


class Favorite(models.Model):
    book = models.ForeignKey('Book')
    user = models.ForeignKey('authentication.User')

class Tag(models.Model):
    name = models.CharField(max_length=100)

class SelfdefinedTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name