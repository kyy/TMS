from django.contrib.auth.models import User, update_last_login
from django.contrib.auth import authenticate, user_logged_in, login, logout
from rest_framework import generics, status, renderers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class RegisterAPIView(generics.CreateAPIView):
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class LoginAPIView(generics.UpdateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        try:
            token, created = Token.objects.get_or_create(user=user)
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        finally:
            login(request, user)

        return Response(
            data={'message': 'User logged in successfully', 'token': token.key},
            status=status.HTTP_200_OK
        )


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    model = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            logout(request)
        finally:
            return Response(status=status.HTTP_200_OK)
        # try:
        #     token = Token.objects.get(user=request.user)
        #     token.delete()
        #     return Response({"detail": "Successfully logged out."},
        #                     status=status.HTTP_200_OK)
        # except Token.DoesNotExist:
        #     return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
