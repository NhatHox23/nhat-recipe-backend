from django.test import TestCase

from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Test creating a new user with an email is successful"""
        email = 'test@nhat.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@NHAT.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password="test123"
        )
        print(user.email)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        email = 'test'
        password = ""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email,
                password=password
            )

    def test_create_super_user_successfully(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            email="test_super@nhat.com",
            password="Test123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
