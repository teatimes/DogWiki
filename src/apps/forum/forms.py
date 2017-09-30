# -*- coding: utf-8 -*-

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from django.db.models import Q
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from functools import reduce
import django_filters

from .models import Post, Comment

class AddPostForm(ModelForm):

    title = forms.CharField(
        label=_('Title')
    )

    text = forms.CharField(
        label=_('Text'),
        widget=forms.Textarea(),
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.layout = Layout(
        Field('title', css_class='input-xlarge'),
        Field('text', rows='10', css_class='input-small'),
    )


    def clean(self):
        super(AddPostForm, self).clean()
        cleaned_data = self.cleaned_data

        return cleaned_data


    class Meta:
        model = Post
        fields = ['title', 'text']


class AddCommentForm(ModelForm):

    model = Comment

    text = forms.CharField(
        label=_('Tekst'),
        widget=forms.Textarea(),
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.layout = Layout(
        Field('text', rows='10', css_class='input-small'),
    )


    class Meta:
        model = Comment
        fields = ['text']


class PostFilter(django_filters.FilterSet):


    def filter_keyword(self, queryset, value):

        if value != "":
            if " " in value:
                list = value.split(" ")

                try:
                    queryset = []
                    for post in Post.objects.all():
                        for word in list:
                            if word.lower() in (post.title.lower() or post.text.lower()):

                                queryset.append(post)
                    # TODO: not working, but a better solution
                    #queryset = Post.objects.filter(lambda x: x, [Q(title__contains=word) or Q(text__contains=word) for word in list])
                except Exception:
                    queryset = Post.objects.all()
            else:
                queryset = Post.objects.filter(Q(title__contains=value) or Q(text__contains=value))

        else:
            queryset = Post.objects.all()

        return queryset


    text = django_filters.CharFilter(label='Søkeord', method=filter_keyword)

    class Meta:
        model = Post
        fields = {
            'text'
        }