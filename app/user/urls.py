from django.urls import path
from .views import CreateUserAPI, CreateTokenView, ManageUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserAPI.as_view(), name="create"),
    path('token/', CreateTokenView.as_view(), name='create-token'),
    path('me/', ManageUserView.as_view(), name="me")
]
