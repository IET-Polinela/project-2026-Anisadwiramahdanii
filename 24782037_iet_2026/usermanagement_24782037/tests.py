from django.test import TestCase

from .forms import CitizenRegistrationForm


class CitizenRegistrationFormTests(TestCase):
    def test_registration_form_creates_citizen_role_by_default(self):
        form = CitizenRegistrationForm(
            data={
                'username': 'citizen01',
                'email': 'citizen01@example.com',
                'password1': 'LabSession6Pass123!',
                'password2': 'LabSession6Pass123!',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_member)
