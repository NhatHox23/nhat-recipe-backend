from django.db import models

from django.conf import settings


# Create your models here.

class Tag(models.Model):
    """Tag models use for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
