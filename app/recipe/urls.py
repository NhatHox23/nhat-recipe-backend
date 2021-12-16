from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagListAPI

# router = DefaultRouter()
# router.register('tags', views.TagListAPI)

app_name = 'recipe'

urlpatterns = [
    path('list/', TagListAPI.as_view(), name="list-tag")
]
