from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class LoginAPIView(generics.UpdateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.queryset
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj
