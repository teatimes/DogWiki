import logging

from django.core.urlresolvers import reverse
from django.test import TestCase

from src.apps.authentication import LoginForm, RegisterForm

class UserRegistrationTestCase(TestCase):

    
    def setUp(self):
        self.logger = logging.getLogger(__name__)

    
    def test_registration_form(self):
        self.logger.debug("Testing registration form")
        form_data = {
            'first_name': 'Ola',
            'last_name': 'Nordmann',
            'email': 'ola@test.com',
            'password': '123qwe123qwe',
            'repeat_password': '123qwe123qwe'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())


# TODO: not working
class UserLoginTestCase(TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)
        form_data = {
            'first_name': 'Ola',
            'last_name': 'Nordmann',
            'email': 'ola@test.com',
            'password': '123qwe123qwe',
            'repeat_password': '123qwe123qwe'
        }
        form = RegisterForm(data=form_data)

    def test_login(self):
        self.logger.debug("Testing login form")
        form_data = {
            'email': 'ola@test.com',
            'password': '123qwe13qwe'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


# TODO: not tested
class AuthenticationURLTestCase(TestCase):
    def test_auth_login_view(self):
        url = reverse('auth_register')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_register_view(self):
        url = reverse('auth_login')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_recover_view(self):
        url = reverse('auth_logout')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
