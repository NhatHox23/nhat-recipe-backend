from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagListAPI, TagCreateAPI

# router = DefaultRouter()
# router.register('tags', views.TagListAPI)

app_name = 'recipe'

urlpatterns = [
    path('tag/list/', TagListAPI.as_view(), name="list-tag"),
    path('tag/create/', TagCreateAPI.as_view(), name="create-tag")
]
