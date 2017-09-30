# -*- coding: utf-8 -*-

from django.db import models


class Post(models.Model):

    title = models.CharField('title', max_length=50, blank=False)
    text = models.CharField('text', max_length=500, blank=False)
    author = models.ForeignKey('authentication.User', related_name='post_author', null=True)
    posted = models.DateField(auto_now=True)


class Comment(models.Model):

    text = models.CharField('text', max_length=500, blank=False)
    author = models.ForeignKey('authentication.User', related_name='comment_author', null=True)
    posted = models.DateField(auto_now=True)
    votes = models.IntegerField(default=0)


class CommentToPost(models.Model):

    post = models.ForeignKey('Post', related_name='comment_to_post_post')
    comment = models.ForeignKey('Comment', related_name='comment_to_post_comment')


class PostVote(models.Model):

    post = models.ForeignKey('Post', related_name='post_vote_post')
    user = models.ForeignKey('authentication.User', related_name='post_vote_user')


class CommentVote(models.Model):

    comment = models.ForeignKey('Comment', related_name='comment_vote_comment')
    user = models.ForeignKey('authentication.User', related_name='comment__vote_user')

   

