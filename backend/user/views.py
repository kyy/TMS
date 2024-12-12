from dbm import error

from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate, user_logged_in, login, logout
from psycopg import IntegrityError
from rest_framework import generics, status, renderers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .ex.permissions import IsAnon
from .serializers import RegisterSerializer, AuthSerializer, ChangePasswordSerializer, User


class RegisterAPIView(generics.CreateAPIView):
    # renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAnon,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.create_user(**serializer.validated_data)
            return Response(
                data='Регистрация прошла успешно',
                status=status.HTTP_200_OK
            )
        except IntegrityError as e:
            return Response(
                data={'message': 'Не удалось создать нового пользователя', 'error': e},
                status=status.HTTP_403_FORBIDDEN
            )


class AuthAPIView(generics.UpdateAPIView):
    serializer_class = AuthSerializer
    permission_classes = (IsAnon,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        try:
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response(
                data='Пользователь не обнаружен',
                status=status.HTTP_403_FORBIDDEN
            )
        finally:
            login(request, user)
        return Response(
            data='Вход выполнен',
            status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            logout(request)
        finally:
            return Response(
                data='Выход выполнен',
                status=status.HTTP_200_OK
            )


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
        serializer.is_valid(raise_exception=True)
        try:
            user.set_password(serializer.data.get("new_password"))
            user.save()
        except IntegrityError as e:
            return Response(
                data={'message': 'Не удалось сменить пароль', 'error': e},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            data='Новый пароль установлен',
            status=status.HTTP_202_ACCEPTED
        )
