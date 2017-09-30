from django.test import TestCase

from src.apps.authentication import RegisterForm
from src.apps.profile import EditProfileForm

# Create your tests here.
class EditUserProfileTestCase(TestCase):

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

    def test_edit_profile(self):
        self.logger.debug("Testing edit profile form")
        form_data = {
        	'birth_year': '1980',
        	# TODO: how to test imageField?
        	'work_title': 'stud',
        	'work_place': 'Trondheim',
        	'competence': 'kognitiv terapi, psykoanalyse',
        	'work_field': 'treatment'
        }
        form = EditProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

