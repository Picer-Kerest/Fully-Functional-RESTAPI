from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ModelSerializer
from .models import User


class RegisterSerializer(ModelSerializer):
    """
    write_only - это атрибут поля в Django REST framework, который указывает,
    что это поле может использоваться только для записи данных и не должно быть возвращено в ответе на запросы GET.
    Поле с атрибутом "write_only" может быть полезно, например,
    когда вы хотите получить данные от пользователя, но не хотите,
    чтобы эти данные были возвращены при просмотре записи
    """
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        """
        attrs - это словарь атрибутов, представляющих данные, которые были отправлены клиентом
        isalnum Возвращает флаг, указывающий на то, содержит ли строка только цифры и/или буквы.
        """
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            # raise serializers.ValidationError(
            #     self.default_error_messages)
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(ModelSerializer):
    """
    Пользователь может войти, но не может изменить username & tokens через API
    write_only=True Делаем так, чтобы поле не возвращалось при сериализации объекта
    """
    email = serializers.EmailField(max_length=255, min_length=5)
    username = serializers.CharField(max_length=64, min_length=3, read_only=True)
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=255, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens']
    #     Какие поля будут сериализованы

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class ResetPasswordSerializer(ModelSerializer):
    email = serializers.EmailField(min_length=5)

    class Meta:
        fields = ['email']


