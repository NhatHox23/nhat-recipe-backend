from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
ME_URL = reverse("user:me")


def create_user(**kwargs):
    """Helper function for creating user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserAPITest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'Test@nhat.com',
            'password': 'testpass',
            'name': 'Unit Test'
        }
        res = self.client.post(CREATE_USER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_existed_user(self):
        """Test creating existing user"""
        payload = {
            'email': 'Test@nhat.com',
            'password': 'testpass',
            'name': 'Unit Test'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'Test@nhat.com',
            'password': 'pw',
            'name': 'Unit Test'
        }

        res = self.client.post(CREATE_USER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthenticated(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test API request that required authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@nhat.com',
            password='password',
            name='Private Test'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_user_authenticated(self):
        """Test that retrieve user with log_in"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'Updated Test', 'password': 'updatepassword'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
