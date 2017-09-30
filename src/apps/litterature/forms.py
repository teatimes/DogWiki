# -*- coding: utf-8 -*-

import re

import django_filters

from amazon.api import AmazonAPI


from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from django import forms
from django.conf import settings
from django.core import serializers
from django.utils.translation import ugettext as _

from .models import Book, Author, Topic, SelfdefinedTag, RATING_CHOICES


class AddBookForm(forms.Form):

    search_field = forms.CharField(
        label=_("ISBN-10 or title"),
        max_length=100,
        error_messages={'invalid': 'Unvalid ISBNnr. Must be in the format xxx-xxxxxxxxxx or xxxxxxxxx'}
    )

    training_topics = forms.ModelMultipleChoiceField(
        label=_("Terapi-nøkkelord"),
        widget=forms.SelectMultiple(),
        queryset=Topic.objects.filter(belong_to='therapy'),
        help_text="Hold CTRL in to pick one or more, or remove choosen keywords",
        required=False
    )

    behaviour_topics = forms.ModelMultipleChoiceField(
        label=_("Basalfag-nøkkelord"),
        widget=forms.SelectMultiple(),
        queryset=Topic.objects.filter(belong_to='course'),
        help_text="Hold CTRL in to pick one or more, or remove choosen keywords",
        required=False
    )

    selfdefined_tags = forms.CharField(
        label=_("Tags"),
        max_length=100,
        help_text="Separate them with comma.",
        required=False
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.add_input(Submit('search-btn', 'Finn bok', css_class="btn-primary"))
    helper.layout = Layout(
        Field('search_field'),
        Field('training_topics'),
        Field('behaviour_topics'),
        Field('selfdefined_tags')
    )


    def get_author_list(self, authors):
        author_list = ""
        for author in authors:
            author_list += author + ", "
        return author_list[:-2]


    def get_author(self, author):
        author_list = []

        authors = author.split(",")
        for author in authors:
            name = author.split(" ")
            first = " ".join(name[:-1])
            last = name[-1]

            author, created = Author.objects.get_or_create(first_name=first, last_name=last)
            if created:
                author.save()
            author_list.append(author)

        return author_list


    def validate_search_phrase(self, search_phrase):
        access_key = getattr(settings, 'AMAZON_ACCESS_KEY')
        secret_key = getattr(settings, 'AMAZON_SECRET_KEY')
        tag = getattr(settings, 'AMAZON_ASSOC_TAG')

        amazon = AmazonAPI(access_key, secret_key, tag)

        isbn_regex = re.compile('[0-9]{10}$')

        # If search on isbn
        if self.cleaned_data['search_field'].strip("-").isdigit():
            isbn = self.cleaned_data['search_field']
            if isbn_regex.match(isbn):
                try:
                    am_book = amazon.lookup(ItemId=isbn)
                    return am_book
                except Exception as e:
                    print("Invalid ISBN: ", isbn)
                    self.add_error('isbn', 'Not valid ISBNnr.')
                    return None
            else:
                print("Invalid ISBN: ", isbn)
                self.add_error('search_field', 'Not valid ISBNnr. Must be in the format xxxxxxxxx')
                return None
        # Elif search on title or author
        else:
            am_books = amazon.search(Keywords=search_phrase, SearchIndex='Books')

            search_result = []
            count = 1
            for book in am_books:
                if count > 5:
                    break
                else:
                    book_info = {
                        'id': count,
                        'title': book.title,
                        'published': book.publication_date.year,
                        'isbn': book.isbn,
                        'authors': self.get_author_list(book.authors),
                        'cover_url': book.large_image_url,
                        'offer_url': book.offer_url,
                        'length': book.pages,
                    }

                    search_result.append(book_info)
                    count += 1
            return search_result

    def validate_tags(self, tags):
        name_list = tags.split(",")
        tag_list = []
        for tag in name_list:
            if len(tag) <= 2:
                self.add_error('selfdefined_tags', 'Nøkkelord må være lengre enn 2 tegn.')
            elif any(char.isdigit() for char in tag):
                self.add_error('selfdefined_tags', 'Nøkkelord kan ikke inneholde tall.')
            t, created = SelfdefinedTag.objects.get_or_create(name=tag)
            t.save()
            tag_list.append(t.pk)
        return tag_list

    def clean(self):
        super(AddBookForm, self).clean()

        cleaned_data = self.cleaned_data

        if self.is_valid():
            
            if not self.validate_search_phrase(cleaned_data['search_field']) is None:
                cleaned_data['am_book'] = self.validate_search_phrase(cleaned_data['search_field'])
            
            cleaned_data['selfdefined_tags'] = self.validate_tags(cleaned_data['selfdefined_tags'])
            return cleaned_data
        else:
            return super(AddBookForm, self).clean()

    # TODO: can this be removed?
    def save(self):
        book = super(AddBookForm, self).save()
        book.save()
        return book

    # To attach additional options/metadata to the form
    class Meta:
        model = Book
        fields = ['search_field', 'therapy_topics', 'course_topics', 'diagnose_topics', 'selfdefined_tags']


class BookFilter(django_filters.FilterSet):
    

    def filter_keyword(self, queryset, value):

        if value != "":
            if " " in value:
                list = value.split(" ")

                try:
                    queryset = []
                    for book in Book.objects.all():
                        for word in list:
                            if word.lower() in (book.title.lower() or book.author_list().lower()):
                                queryset.append(post)
                except Exception:
                    queryset = Book.objects.all()
            else:
                queryset = Book.objects.filter(Q(title__contains=value) or Q(authors__contains=value))

        else:
            queryset = Book.objects.all()

        return queryset


    title = django_filters.CharFilter(label='Search word', method=filter_keyword)
    topic = django_filters.ModelMultipleChoiceFilter(
        label='Topics', 
        widget=forms.CheckboxSelectMultiple,
        queryset=Topic.objects.all()    
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.add_input(Submit('filter-books', 'Search', css_class="btn-primary"))
    helper.layout = Layout(
        Field('title', placeholder="Search for book, title or topic."),
        Field('topic'),
    )

    class Meta:
        model = Book
        fields = {
            'title',
            'topic',
        }


class AddReviewForm(forms.ModelForm):

    title = forms.CharField(
        label=_("Tittel"),
        max_length=50,
    )

    review = forms.CharField(
        label=_("Review"),
        max_length=500,
    )

    rating = forms.ChoiceField(
        label=_("Rating"),
        choices=RATING_CHOICES
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.add_input(Submit('add-review-btn', 'Publiser review', css_class="btn-primary"))
    helper.layout = Layout(
        Field('title', css_class='col-sm-2'),
        Field('review', rows='5', css_class='input-small'),
        Field('rating', css_class='input-medium'),
    )

    def clean(self):
        super(AddReviewForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data
        return cleaned_data


    def save(self):
        review = super(AddReviewForm, self).save()
        review.save()
        return

    # To attach additional options/metadata to the form
    class Meta:
        model = Book
        fields = ['title', 'review', 'rating']
