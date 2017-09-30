import logging

from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from .forms import LoginForm, RegisterForm


@sensitive_post_parameters()
def login(request):
    redirect_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, _('You are now logged in.'))
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            return HttpResponseRedirect('/')
        else:
            form = LoginForm(request.POST, auto_id=True)
    else:
        form = LoginForm()

    response_dict = {'form': form, 'next': redirect_url}
    return render(request, 'authentication/login.html', response_dict)


def logout(request):
    auth.logout(request)
    messages.success(request, _("Du er nå logget ut."))
    return HttpResponseRedirect('/')


@sensitive_post_parameters()
def register(request):
    log = logging.getLogger(__name__)

    if request.user.is_authenticated():
        messages.error(request, _('Registration of new user require that you are logged out.'))
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                cleaned = form.cleaned_data

                try:
                    user = form.save(commit=False)
                    user.save()

                    try:
                        user.profile_image = request.FILES['profile_image']
                    except:
                        print("missing profile image")

                    messages.success(
                        request,
                        _('Registration was sucessful.')
                    )

                    # Go to frontpage
                    return HttpResponseRedirect('/login/')
                except Exception as e:
                    print("Something went wrong creating user:", e)

            else:
                form = RegisterForm(request.POST, auto_id=True)
        else:
            form = RegisterForm()

        return render(request, 'authentication/register.html', {'form': form, })
