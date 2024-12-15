from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.RegisterAPIView.as_view()),
    path('auth/', views.AuthAPIView.as_view()),
    path('lout/', views.LogoutAPIView.as_view()),
    path('chpswd/', views.ChangePasswordAPIView.as_view()),
    path('csrf/', views.set_csrf_token),
]
