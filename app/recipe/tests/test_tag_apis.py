from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Tag
from recipe.serializers import TagSerializer

from core.tests.utils import sample_tag, sample_user

TAG_LIST_URL = reverse('recipe:list-tag')
TAG_CREATE_URL = reverse('recipe:create-tag')


class PublicTagListAPI(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.tag = sample_tag(user=self.user)
        self.client = APIClient()
        self.payload = {
            "user": self.user.id,
            "name": "Unit Test Tag"
        }

    def test_list_tag_unauthenticated(self):
        """Test listing tag without log-in"""
        res = self.client.get(TAG_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tag_unauthenticated(self):
        """Test creating tag without log-in"""
        res = self.client.post(TAG_CREATE_URL, self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagListApiTest(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.tag = sample_tag(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.payload = {
            "user": self.user.id,
            "name": "Unit Test Tag"
        }

    def test_list_tag_authenticated(self):
        """Test listing tag with log-in"""
        res = self.client.get(TAG_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tags = TagSerializer(Tag.objects.all(), many=True)

        self.assertEqual(res.data, tags.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = sample_user(email="test2@nhat.com")
        sample_tag(user=user2, name="test tag 2")
        res = self.client.get(TAG_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], self.tag.name)

    def test_create_tag_authenticated(self):
        """Test creating tag withd log-in"""
        res = self.client.post(TAG_CREATE_URL, self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_tag = Tag.objects.get(**self.payload)
        self.assertEqual(res.data["name"], created_tag.name)

    def test_create_tag_invalid_payload(self):
        invalid_payload = {}
        res = self.client.post(TAG_CREATE_URL, invalid_payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
