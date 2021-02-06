from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import include, path

from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('', include('booking_portal.urls')),
    # path('booking/', include('booking_portal.urls')),
    path('admin/', admin.site.urls),
    path('auth/password_reset/', PasswordResetView.as_view(form_class=CustomPasswordResetForm)),
    path('auth/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm)),
    path('auth/', include('django.contrib.auth.urls')),
]
