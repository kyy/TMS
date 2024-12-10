from django.urls import path

from .views import LoginAPIView, RegisterAPIView, ChangePasswordAPIView, LogoutAPIView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('chpswd/', ChangePasswordAPIView.as_view()),
]
