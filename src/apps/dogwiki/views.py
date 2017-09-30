# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from src.apps.authentication.models import Action, Follow

from .forms import ContactForm


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        followed_objects = Follow.objects.filter(following=self.request.user)
        print("Followed objects: ", followed_objects)
        followed_users = []
        for object in followed_objects:
            followed_users.append(object.followed)

        context['action_list'] = Action.objects.filter(user__in=followed_users).order_by('-date')[:30]
        print("Action list: ", context['action_list'])
        return context


class ContactUsView(TemplateView):
    template_name = 'dogwiki/contact_us.html'
    form_class = ContactForm


    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cleaned = form.cleaned_data
            send_mail(
                cleaned['subject'],
                cleaned['message'],
                ['doraoline@gmail.com'],
                fail_silently=True
            )
            return HttpResponseRedirect("/email_sent/")
        return render(request, self.template_name, {'form': form})


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))

    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))

    response.status_code = 500
    return response


def handler403(request):
    response = render_to_response('403.html', {}, context_instance=RequestContext(request))

    response.status_code = 403
    return response


def handler400(request):
    response = render_to_response('400.html', {}, context_instance=RequestContext(request))

    response.status_code = 400
    return response
