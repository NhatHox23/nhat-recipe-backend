from django.test import TestCase

from django.urls import reverse

from rest_framework.test import APIClient

from rest_framework import status

from .test_user_api import create_user

CREATE_TOKEN_URL = reverse("user:create-token")


class PublicTokenAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'Test@nhat.com',
            'password': 'Testpassword'
        }
        create_user(**self.payload)

    def test_create_token_for_user(self):
        """Test creating token for user"""
        res = self.client.post(CREATE_TOKEN_URL, self.payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        payload_invalid_password = self.payload.copy()
        payload_invalid_password['password'] = 'wrong_password'
        res = self.client.post(CREATE_TOKEN_URL, payload_invalid_password)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload_invalid_email = self.payload.copy()
        payload_invalid_email['email'] = 'NoEmail@nhat.com'
        res = self.client.post(CREATE_TOKEN_URL, payload_invalid_email)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_fields(self):
        """Test that email and password is required"""
        res = self.client.post(CREATE_TOKEN_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


