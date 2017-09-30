# -*- coding: utf-8 -*-

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from django.contrib import auth
from django.utils.translation import ugettext as _

from .models import User as User


class LoginForm(forms.Form):
    
    email = forms.CharField(
        widget=forms.TextInput(),
        label=_("Brukernavn eller epost"),
        max_length=100
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Passord")
    )

    user = None

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.add_input(Submit('login', 'Logg inn', css_class="btn-primary"))
    helper.layout = Layout(
        Field('topic', style="padding: 10px;"),
        Field('search_field'),
        Field('tags')
    )

   
    def clean(self):
        if self._errors:
            return

        email = self.cleaned_data['email'].lower()

        user = auth.authenticate(username=email, password=self.cleaned_data['password'])

        if user:
            self.user = user
        else:
            self._errors['email'] = self.error_class(
                [_("Brukeren eksisterer ikke, eller feil passord.")]
            )
        return self.cleaned_data

   
    def login(self, request):
        if self.is_valid():
            auth.login(request, self.user)
            return True
        return False

    
    class Meta:
        fields = ['email', 'password', 'login']


class RegisterForm(forms.ModelForm):

    first_name= forms.CharField(
        label=_("Fornavn"),
        max_length=50,
    )

    last_name  = forms.CharField(
        label=_("Etternavn"),
        max_length=50,
    )

    email = forms.CharField(
        label=_("Epost"),
        max_length=50
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Passord")
    )
    
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Gjenta passord")
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.add_input(Submit('register', 'Registrer deg', css_class="btn-primary"))
    helper.add_input
    helper.layout = Layout(
        Field('first_name'),
        Field('last_name'),
        Field('email'),
        Field('password'),
        Field('repeat_password'),
    )


    def clean(self):
        super(RegisterForm, self).clean()

        if self.is_valid():
            print("Form is valid")
            cleaned_data = self.cleaned_data

            # Check passwords
            if cleaned_data['password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class([_("Passordene er ikke like.")])

            email = cleaned_data['email'].lower()

            return cleaned_data


    def save(self, commit):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


    # To attach additional options/metadata to the form
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'repeat_password']
