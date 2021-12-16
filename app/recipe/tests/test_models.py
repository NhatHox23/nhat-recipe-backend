from django.test import TestCase

from core.tests.utils import sample_user

from ..models import Tag


class TagModelTest(TestCase):

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(
            user=sample_user(),
            name='Meat Lover'
        )
        self.assertEqual(str(tag), tag.name)

