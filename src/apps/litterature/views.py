# -*- coding: utf-8 -*-

import datetime

from amazon.api import AmazonAPI
from src.apps.authentication.models import Action
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView, DetailView
from django.views.generic.edit import FormMixin

from .forms import AddBookForm, BookFilter, AddReviewForm
from .models import Book, Author, Topic, Review, Read, Recommended, Tag, SelfdefinedTag


@method_decorator(login_required, name='dispatch')
class LitteratureListView(ListView):

    model = Book
    template_name = "litterature/litterature_list.html"

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LitteratureListView, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        context['filter'] = BookFilter(self.request.GET, queryset=Book.objects.all())
        return context


@method_decorator(login_required, name='dispatch')
class BookDetailView(DetailView, FormMixin):

    model = Book
    form_class = AddReviewForm
    template_name = "litterature/book_detail.html"


    def get_mean_rating(self, reviews):
        count = 0
        total = 0
        if len(reviews) == 0:
            return 0
        for review in reviews:
            count += 1
            total += review.rating
        return total/count


    # Because of the reviewForm
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book = Book.objects.get(pk=self.kwargs['pk'])
        context['book'] = book
        context['pk'] = self.kwargs['pk']
        context['review_list'] = Review.objects.filter(book=book)
        #context['rating'] = self.get_mean_rating(book.review.all())
        context['form'] = self.get_form()
        return context


    def post(self, request, pk):

        if request.POST.get('add-review-btn'):
            form = self.form_class(request.POST)

            if form.is_valid():
                print("Review form is valid")
                cleaned = form.cleaned_data
                # Creates an object from the form, but don't save it the database

                review = Review()
                review.save()

                review.title = cleaned['title']
                review.author = request.user
                review.review = cleaned['review']
                review.published = datetime.date.today()
                review.book = self.get_object()
                review.rating = cleaned['rating']

                review.save()

        elif request.POST.get('read-btn') or request.POST.get('rec-btn'):
            user = request.user
            book = Book.objects.get(pk=pk)

            if request.POST.get('read-btn'):

                if Read.objects.filter(book=book, user=user).exists():
                    rel = Read.objects.get(book=book, user=user)
                    rel.delete()
                    print("Remove book from read")
                else:
                    rel = Read(book=book, user=user)
                    rel.save()
                    print("Add book to read")
                    user_name = user.get_full_name()
                    action = Action(
                        user=user,
                        action=user_name + " har lest " + book.title,
                    )
                    action.save()

            elif request.POST.get('rec-btn'):

                if Recommended.objects.filter(book=book, user=user).exists():
                    rel = Recommended.objects.get(book=book, user=user)
                    rel.delete()
                    print("Remove book from recommended")
                else:
                    rel = Recommended(book=book, user=user)
                    rel.save()
                    print("Add book to recommended")
                    user_name = user.get_full_name()
                    action = Action(
                        user=user,
                        action=user_name + " anbefaler " + book.title,
                    )
                    action.save()

        else:
            print("None of the buttons")

        return HttpResponseRedirect("{% url 'book-detail' book.pk %}")

@method_decorator(login_required, name='dispatch')
class AddBookView(FormView):
    form_class = AddBookForm
    template_name = 'litterature/add_litterature.html'

    def create_book(self, am_book, topics, selfdefined_tags):
        book = Book()
        book.save()
        try:
            authors = am_book['authors']
            authors = authors.split(", ")
            for author in authors:
                fullname = author.split(" ")
                
                first_name = ""
                length = len(fullname)
                i = 0
                while i < length - 1:
                    if i == 0:
                        first_name = fullname[i]
                    else:
                        first_name += " " + fullname[i]
                    i += 1
                last_name = fullname[len(fullname) - 1]
                author, created = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
                author.save()
                book.author.add(author)
            book.title = am_book['title']
            book.published = am_book['published']
            book.isbn = am_book['isbn']
            book.shop_url = am_book['offer_url']

            for pk in topics:
                book.topic.add(Topic.objects.get(pk=pk))
            for pk in selfdefined_tags:
                book.selfdefined_tags.add(SelfdefinedTag.objects.get(pk=pk))

            book.cover_url = am_book['cover_url']

            book.length = am_book['length']

            book.save()
        except:
            print("Something went wrong in create_book")
            book.delete()


    def get_author_list(self, authors):
        author_list = ""
        for author in authors:
            author_list += author + ", "
        print("AUthor-list: ", author_list)
        return author_list[:-2]


    # Display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'search_result': None})


    def post(self, request, search_result = None):
        form = self.form_class(request.POST)

        if 'search-btn' in request.POST:
            if form.is_valid():

                search_result = []

                cleaned = form.cleaned_data
                
                if cleaned['am_book'] == None:
                    pass
                else:
                    request.session['search_result'] = cleaned['am_book']
                    
                    topics_pk = []

                    for topic in cleaned['therapy_topics']:
                        topics_pk.append(topic.pk)

                    for topic in cleaned['course_topics']:
                        topics_pk.append(topic.pk)

                    for topic in cleaned['diagnose_topics']:
                        topics_pk.append(topic.pk)

                    request.session['topics'] = topics_pk
                    request.session['selfdefined_tags'] = cleaned['selfdefined_tags'] 
                
                return render(request, self.template_name, {'form': form, 'search_result': cleaned['am_book']})
        # Else if a book-button is clicked
        else:
            search_result = request.session.get('search_result')
            topics = request.session.get('topics')
            selfdefined_tags = request.session.get('selfdefined_tags')
            for i in range(1,5):
                if str(i) in request.POST:
                    print(i, " was in request.POST")
                    self.create_book(search_result[i-1], topics, selfdefined_tags)
                    break

            return HttpResponseRedirect('/litterature/')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class AuthorDetailView(DetailView):
    model = Author
    template_name = "litterature/view_author.html"

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        return context
