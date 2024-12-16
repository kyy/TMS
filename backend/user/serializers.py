from django.contrib.auth import authenticate
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }


class AuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def validate(self, data):
        password = data.get('password', None)
        email = data.get('email', None)
        username = get_object_or_404(User.objects.all(), email=email)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(detail='Пользователь не найден или не активен, возможно неверный пароль!',
                                              code=404)
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

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = self.context['request'].user

        if old_password == new_password:
            raise serializers.ValidationError(detail='Ваш новый пароль совпадает со старым!', code=403)

        elif not user.check_password(old_password):
            raise serializers.ValidationError(detail='Текущий пароль введен не верно', code=203)

        return data
