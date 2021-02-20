from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetConfirmView,
                                       PasswordResetView, PasswordChangeView)
from django.urls import path, include

from .forms import (CustomLoginForm, CustomPasswordResetForm,
                    CustomSetPasswordForm, CustomPasswordChangeForm)

urlpatterns = [
    path('login/', LoginView.as_view(form_class=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'password_change/',
        PasswordChangeView.as_view(form_class=CustomPasswordChangeForm),
        name='password_change'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            email_template_name='email/registration/password_reset_email.txt',
            html_email_template_name='email/registration/password_reset_email.html',
            subject_template_name='email/registration/password_reset_subject.txt'
        ),
        name='password_reset',
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm),
        name='password_reset_confirm',
    ),
    path('', include('django.contrib.auth.urls')),
]
