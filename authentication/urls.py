from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    VerifyEmail,
    LoginApiView,
    ResetPasswordStartView,
    ResetPasswordDoneView,
    SetNewPasswordView,
    LogoutView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('start-reset-password/', ResetPasswordStartView.as_view(), name='reset-password-start'),
    path('done-reset-password/<uidb64>/<token>/', ResetPasswordDoneView.as_view(), name='reset-password-done'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
]

