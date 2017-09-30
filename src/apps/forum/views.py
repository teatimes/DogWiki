# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, render_to_response, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, DetailView
from django.views.generic.edit import FormMixin

from .forms import AddPostForm, AddCommentForm, PostFilter
from .models import Post, CommentToPost, Comment


def number_of_comments(self):

    counts = {}
    for post in Post.objects.all():
        counts[post.pk] = len(CommentsToPost.objects.filter(post=post))
    return counts


@method_decorator(login_required, name='dispatch')
class ForumListView(ListView):

    model = Post
    template_name = 'forum/forum_list.html'


    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset


    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        context['filter'] = PostFilter(self.request.GET, queryset=Post.objects.all())
        context['comments_counts'] = number_of_comments(self)

        return context


@method_decorator(login_required, name='dispatch')
class ForumPostDetailView(DetailView, FormMixin):

    model = Post
    form_class = AddCommentForm
    template_name = 'forum/forum_post.html'


    def get_comments(self, post):
        comment_rel = CommentToPost.objects.filter(post=post)
        comments = []
        for comment in comment_rel:
            comments.append(comment.comment)
        comments.sort(key=lambda x: x.votes, reverse=True)
        return comments


    def get_context_data(self, **kwargs):
        context = super(ForumPostDetailView, self).get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        context['post'] = post
        context['pk'] = self.kwargs['pk']
        context['comment_list'] = self.get_comments(post)
        context['comment_counts'] = number_of_comments(self)
        context['form'] = self.get_form()
        return context


    def post(self, request, pk):
        form = self.form_class(request.POST)
        post = Post.objects.get(pk=pk)

        if (request.POST.get('upvote-btn') or request.POST.get('downvote-btn')):

            if request.POST.get('upvote-btn'):
                comment_pk = request.POST.get('upvote-btn')
                comment = Response.objects.get(pk=comment_pk)
                comment.votes += 1

            elif request.POST.get('downvote-btn'):
                comment_pk = request.POST.get('downvote-btn')
                comment = Response.objects.get(pk=comment_pk)
                comment.votes -= 1

            comment.save()

            return HttpResponseRedirect("{% url 'forum_post' pk %}")
        else:
            if form.is_valid():
                cleaned = form.cleaned_data
                if request.POST.get('post-btn'):
                    try:
                        comment = form.save()
                        comment.text = cleaned['text']
                        comment.author = request.user
                        comment.save()

                        rtp = ResponseToPost(post=Post.objects.get(pk=pk), comment=comment)
                        rtp.save()

                        return HttpResponseRedirect("{% url 'forum_post' pk %}")

                    except Exception as e:
                        print("Could not save review: ", e, type(e))
                return HttpResponseRedirect("{% url 'forum_post' pk %}")
        return render(request, self.template_name, {'form': form, 'pk': pk})


@method_decorator(login_required, name='dispatch')
class CreatePostFormView(FormView):

    form_class = AddPostForm
    template_name = 'forum/create_post.html'


    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cleaned = form.cleaned_data
            post = form.save()

            try:
                post.title = cleaned['title']
                post.text = cleaned['text']
                post.author = request.user
                post.save()

                return HttpResponseRedirect('/forum/%s' % post.pk)

            except Exception as e:
                print("Could not save post: ", e, type(e))
                post.delete()

        return render(request, self.template_name, {'form': form})

