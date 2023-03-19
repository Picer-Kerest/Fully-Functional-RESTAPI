from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


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
        username = attrs.get('username', '')

        if not username.isalnum():
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
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        """
        Собственное поле для сериализации.
        Название: get_name
        """
        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens']
        # Какие поля будут сериализованы

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
        model = User
        fields = ['email']


class SetNewPasswordSerializer(ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LogoutSerializer(ModelSerializer):
    refresh = serializers.CharField()

    class Meta:
        model = User
        fields = ['refresh']

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        """
        Добавляем в класс атрибут token со значением введённого токена
        """
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
            # Добавляем токен в чёрный список
        except TokenError:
            self.fail('bad_token')

