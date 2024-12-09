from django.urls import path, include
from .views import LoginAPIView, RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]
