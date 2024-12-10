from datetime import datetime

from django.contrib.auth.models import User, update_last_login

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

