from django.contrib import admin
from django.contrib.auth.views import (LoginView, PasswordResetConfirmView,
                                       PasswordResetView)
from django.urls import include, path

from .forms import (CustomLoginForm, CustomPasswordResetForm,
                    CustomSetPasswordForm)

urlpatterns = [
    path('', include('booking_portal.urls')),
    # path('booking/', include('booking_portal.urls')),
    path('admin/', admin.site.urls),
    path('auth/login/', LoginView.as_view(form_class=CustomLoginForm)),
    path('auth/password_reset/', PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        email_template_name='email/registration/password_reset_email.txt',
        html_email_template_name='email/registration/password_reset_email.html',
        subject_template_name='email/registration/password_reset_subject.txt'
    )),
    path('auth/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm)),
    path('auth/', include('django.contrib.auth.urls')),
]
