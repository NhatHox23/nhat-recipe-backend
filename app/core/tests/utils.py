from django.contrib.auth import get_user_model
from recipe.models import Tag


def sample_user(email='test@nhat.com', password='123'):
    """Helper function to help create user"""
    user = get_user_model().objects.create_user(email=email, password=password)
    return user


def sample_tag(user=None, name="Unit Test"):
    """Helper function to help create tag"""
    if not user:
        user = sample_user()
    tag = Tag.objects.create(user=user, name=name)
    return tag
