from django.urls import path
from .views import LoginAPIView, RegisterAPIView, ChangePasswordAPIView, LogoutAPIView


urlpatterns = [
    path('reg/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('chpswd/', ChangePasswordAPIView.as_view()),
]
