import logging

from django.test import TestCase

from src.apps.litterature import AddBookForm, AddReviewForm
from src.apps.litterature import Topic

# TODO: something wrong with clean_data
class AddBookFormTests(TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)

    def add_book_isbn(self):
        self.logger.debug("Testing add book based on isbn")
        form_data = {
            'isbn': '0393334775',
            'topic': self.topic
        }
        form = AddBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    # TODO: add for title
    # TODO: add for manual

class AddReviewFormTests(TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)

    def add_review(self):

        self.logger.debug("Testing add book based on isbn")
        form_data = {
            'title': 'Review title',
            'review': 'A lot of review text',
            'rating': '3',
        }
        form = AddReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
