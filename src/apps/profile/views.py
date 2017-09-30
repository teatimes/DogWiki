# -*- coding: utf-8 -*-

from src.apps.authentication.models import Follow, Action
from src.apps.authentication.models import User as User
from src.apps.profile.forms import MemberFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView, ListView

from src.apps.litterature.models import Read, Recommended
from src.apps.profile.forms import EditProfileForm


@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return render(request, 'profile/profile_detail.html', {'user': user})

    messages.error(request, 'Du har ikke tilgang til denne profilen')
    return redirect('/')


@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = User
    template_name = 'profile/profile_detail.html'


    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.get_object().pk)
        context['user'] = user
        context['age'] = user.get_age()
        context['pk'] = self.kwargs['pk']
        context['read'] = Read.objects.filter(user=user)
        context['recommend'] = Recommended.objects.filter(user=user)
        return context


    def post(self, request, pk):
        if request.POST.get('follow-btn'):
            print("Following user")

            following = request.user
            followed = User.objects.get(pk=self.get_object().pk)
            if Follow.objects.filter(following=following, followed=followed).exists():
                rel = Follow.objects.get(following=following, followed=followed)
                rel.delete()
                print("Removed following relationship")
            else:
                rel = Follow(following=following, followed=followed)
                rel.save()
                print("Added following relationship")
                following_name = following.get_full_name()
                followed_name = followed.get_full_name()
                action = Action(
                    user=following,
                    action=following_name + " følger " + followed_name,
                )
                action.save()

        return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))


@method_decorator(login_required, name='dispatch')
class EditUserProfileView(FormView):
    model = User
    template_name = 'profile/edit_profile.html'

    #TODO
    #def get_context_data(self, **kwargs):
    #    context = super(EditUserProfileView, self).get_context_data(**kwargs)
    #  context['user'] = User.objects.get(pk=self.get_object().pk)
    #    context['pk'] = self.kwargs['pk']

    #    return context


    def get(self, request, *args, **kwargs):
        form = EditProfileForm(None, instance=request.user)
        return render(request, 'profile/edit_profile.html', {'pk': request.user.pk, 'form': form})


    def post(self, request, pk):
        form = EditProfileForm(request.POST or None, instance=request.user)

        if form.is_valid():
            
            cleaned = form.cleaned_data
            user = request.user
            user.birth_year = cleaned['birth_year']
            user.profile_image = cleaned['profile_image']
            user.work_title = cleaned['work_title']
            user.work_place = cleaned['work_place']
            user.competence = cleaned['competence']
            user.work_fields = cleaned['work_fields']


            user.save()
            form.save()

            return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))
        return render(request, 'profile/edit_profile.html', {'pk': request.user.pk, 'form': form})


@method_decorator(login_required, name='dispatch')
class UserSettingsView(DetailView):
    template_name = 'profile/settings.html'


@method_decorator(login_required, name='dispatch')
class MembersListView(ListView):
    model = User
    template_name = 'profile/members_list.html'

    def get(self, request, *args, **kwargs):
        filter = MemberFilter(request.GET, queryset=User.objects.all())
        return render(request, 'profile/members_list.html', {'filter': filter})

    def get_queryset(self):
        queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MembersListView, self).get_context_data(**kwargs)
        context['members_list'] = User.objects.all()

        context['filter'] = MemberFilter(self.request.GET, queryset=User.objects.all())

        return context


