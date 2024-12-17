from django.contrib.auth.models import update_last_login
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.types import OpenApiTypes
from psycopg import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, AuthSerializer, ChangePasswordSerializer, User
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (AllowAny, )
    http_method_names = ['get']

    @extend_schema(
        summary="CSRF cookie",
        description="CSRF cookie",
        methods=["get"],
        responses={200: OpenApiResponse(description="CSRF cookie set")}
    )
    def get(self, request):
        return Response({"success": "CSRF cookie set"}, status=status.HTTP_200_OK)


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    # renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RegisterSerializer
    http_method_names = ['post']

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя с уникальным email и именем.",
        request=serializer_class,
        methods=["post"],
        parameters=[
            OpenApiParameter(name='email', description='e-mail', required=True, type=OpenApiTypes.EMAIL),
            OpenApiParameter(name='password', description='Пароль', required=True, type=OpenApiTypes.PASSWORD),
            OpenApiParameter(name='username', description='Имя пользоваиеля', required=True, type=str),
        ],
        responses={
            201: OpenApiResponse(response=serializer_class, description="Пользователь успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации"),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.create_user(**serializer.validated_data)
            return Response(
                data={'message': 'Регистрация прошла успешно'},
                status=status.HTTP_201_CREATED
            )
        except IntegrityError as e:
            return Response(
                data={'message': 'Не удалось создать нового пользователя', 'error': e},
                status=status.HTTP_400_BAD_REQUEST
            )


class AuthAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = AuthSerializer
    queryset = User.objects.all()
    http_method_names = ['post', 'get']

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Авторизация пользователя",
        description="",
        request=serializer_class,
        methods=["post"],
        parameters=[
            OpenApiParameter(name='email', description='e-mail', required=True, type=OpenApiTypes.EMAIL),
            OpenApiParameter(name='password', description='Пароль', required=True, type=OpenApiTypes.PASSWORD),
        ],
        responses={
            200: OpenApiResponse(response=serializer_class, description="Пользователь успешно авторизован"),
            401: OpenApiResponse(description="Ошибка данных")
        }
    )
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        try:
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response(
                data={'error', 'Пользователь не обнаружен'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        finally:
            login(request, user)
        return Response(
            data={'success': 'Вход выполнен'},
            status=status.HTTP_200_OK)

    @extend_schema(
        summary="Проверка авторизации",
        description="Возвращает 'email' и 'username'",
        request=serializer_class,
        methods=["get"],
        responses={
            401: OpenApiResponse(description="Не авторизованы"),
            200: OpenApiResponse(description="Успешно авторизованы"),
        }
    )
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'username': request.user.username, 'email': request.user.email}, status=status.HTTP_200_OK)
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        return self.serializer_class(data=request.data).data


class LogoutAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    @extend_schema(
        summary="Разлогиниться",
        description="Выйти из учетной записи",
        methods=["post"],
        responses={
            200: OpenApiResponse(description="Вышли из учетной записи"),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            logout(request)
        finally:
            return Response(
                data={'success': 'Выход выполнен'},
                status=status.HTTP_200_OK
            )


class ChangePasswordAPIView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    model = User
    http_method_names = ['post']

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Смена пароля",
        description="Смена пароля",
        methods=["post"],
        request=serializer_class,
        parameters=[
            OpenApiParameter(name='old_password', description='Старый пароль', required=True, type=OpenApiTypes.PASSWORD),
            OpenApiParameter(name='new_password', description='Новый пароль', required=True, type=OpenApiTypes.PASSWORD),
        ],
        responses={
            202: OpenApiResponse(response=serializer_class, description="Пароль успешно сменен"),
            403: OpenApiResponse(description="Ошибка данных")
        }
    )
    def post(self, request, *args, **kwargs):
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
