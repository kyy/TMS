from django.contrib.auth.models import User, update_last_login
from django.contrib.auth import authenticate, user_logged_in, login, logout
from rest_framework import generics, status, renderers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .ex.permissions import IsAnon
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer


class RegisterAPIView(generics.CreateAPIView):
    # renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAnon,)
    serializer_class = RegisterSerializer


class LoginAPIView(generics.UpdateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAnon,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        try:
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        finally:
            login(request, user)

        return Response(
            data={'message': 'User logged in successfully'},
            status=status.HTTP_200_OK
        )


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            logout(request)
        finally:
            return Response(status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    model = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



