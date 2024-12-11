from django.urls import path
from . import views


urlpatterns = [
    path('reg/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('chpswd/', views.ChangePasswordAPIView.as_view()),
]
