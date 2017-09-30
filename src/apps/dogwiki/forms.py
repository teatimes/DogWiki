# -*- coding: utf-8 -*-

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from django import forms

from django.utils.translation import ugettext as _

class ContactForm(forms.Form):

    subject = forms.CharField(widget=forms.TextInput(), label=_("subject"), required=True, max_length=50)
    message = forms.CharField(widget=forms.Textarea(), label=_("MEssage"), required=True, max_length=1000)

 	# Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-6'
    helper.add_input(Submit('send', 'Send', css_class="btn-primary"))
    helper.layout = Layout(
        Field('subject'),
        Field('message')
    )


    class Meta:
        fields = ['subject', 'message']
