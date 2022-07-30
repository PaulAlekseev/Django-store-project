from django.test import TestCase

from authentication.models import CustomUser
from authentication.forms import RegistrationForm

class TestAuthenticationForm(TestCase):

    def setUp(self):
        self.form_data = {
            'username': 'User1',
            'email': 'User1@mail.ru',
            'password1': 'pASs12345678',
            'password2': 'pASs12345678'
        }
        
    def test_form_is_valid(self):
        """
        Test if form is valid
        """
        form = RegistrationForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_form_on_validation_error(self):
        """
        Test if form allows to validate email that is already taken
        """
        CustomUser.objects.create(
            username='Name', email='User1@mail.ru'
        )
        form = RegistrationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_form_save_method(self):
        """
        Test registration form save method
        """
        form = RegistrationForm(data=self.form_data)
        form.save()

        user = CustomUser.objects.filter(username='User1')
        self.assertTrue(user.exists())
        self.assertFalse(user[0].is_active)
        