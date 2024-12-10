from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate, user_logged_in, login
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True, required=True,
        label='Повторить пароль',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate(self, cleaned_data):
        if cleaned_data['password'] != cleaned_data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return cleaned_data

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', "last_login", "username")
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'last_login': {'read_only': True},

        }

    def validate(self, data):
        password = data['password']
        email = data['email']
        username = User.objects.filter(email=email).get().username
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Пользователь не найден или не активен')
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'username')
        extra_kwargs = {
            'username': {'read_only': True},
        }
