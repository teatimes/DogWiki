# -*- coding: utf-8 -*-

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

import django_filters
from django import forms
from django.utils.translation import ugettext as _

from src.apps.authentication.models import User as User


class ProfileForm(forms.ModelForm):
    class Meta(object):
        model = User

        fields = [
            'username'
        ]

    def clean(self):
        super(ProfileForm, self).clean()

        cleaned_data = self.cleand_data

        return cleaned_data


class MemberFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = User
        fields = [
            'username'
        ]


class EditProfileForm(forms.ModelForm):

    birth_year = forms.IntegerField(
        widget=forms.TextInput(),
        label=_("Fødselsår"),
        #TODO: static, need ot change
        max_value=2000,
        required=False
    )

    profile_image = forms.ImageField(
        label=_("Profilbilde"),
        required=False
    )

    competence = forms.CharField(
        widget=forms.TextInput(),
        label=_("Kompetanse"),
        max_length=50,
        required=False
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.add_input(Submit('edit_user', 'Lagre', css_class="btn-primary"))
    helper.layout = Layout(
        Field('birth_year'),
        Field('profile_image'),
        Field('competence'),
    )


    class Meta:
        model = User
        fields = ['birth_year', 'profile_image','competence']






