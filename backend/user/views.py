from datetime import datetime

from django.contrib.auth.models import User, update_last_login

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status


class RegisterAPIView(generics.CreateAPIView):
   queryset = User.objects.all()
   serializer_class = RegisterSerializer
   permission_classes = (AllowAny,)

class LoginAPIView(generics.CreateAPIView):
   permission_classes = (AllowAny,)
   serializer_class = LoginSerializer

   def post(self, request, *args, **kwargs):
       serializer = self.serializer_class(data=request.data, context={'request': request})
       serializer.is_valid(raise_exception=True)

       return Response({"status": status.HTTP_200_OK})