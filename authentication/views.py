from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from .serializers import (
    EmailVerificationSerializer,
    RegisterSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    SetNewPasswordSerializer,
    LogoutSerializer
)


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    # renderer_classes = (UserRender, )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        # Сериализированные данные

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        domain = get_current_site(request).domain
        relative_link = reverse('email-verify')
        activate_url = f'http://{domain}{relative_link}?token={str(token)}'
        email_body = f'Hi, {user.username}. Please use this link to verify your email\n{activate_url}'
        data = {
            'email_subject': 'Verify your email',
            'email_body': email_body,
            'to_email': user.email}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as ex:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as ex:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'error': 'Unknown error'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """
        serializer.data вернёт сериализованные данные в виде словаря,
        в котором будут ключи 'email', 'username' и 'tokens',
        соответствующие значениям, которые возвращаются из метода validate.
        """
        serializer = self.serializer_class(data=request.data)
        # Далее происходит валидация
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordStartView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            domain = get_current_site(request).domain
            relative_link = reverse('reset-password-done', kwargs={
                'uidb64': uidb64,
                'token': token
            })
            activate_url = f'http://{domain}{relative_link}'
            email_body = f'Hi, {user.username}. Please use this link to reset your password\n{activate_url}'
            data = {
                'email_subject': 'Set New Password link',
                'email_body': email_body,
                'to_email': user.email}
            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response({'error': 'There is no user with this email'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordDoneView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            # force_str instead smart_str. For Django > 3.1
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                    'success': True,
                    'message': 'Credentials is valid',
                    'uidb64': uidb64,
                    'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as ex:
            return Response(
                {'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request):
        # Частичное обновление ресурса
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'You were logged out'}, status=status.HTTP_204_NO_CONTENT)
