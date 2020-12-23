from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('booking_portal.urls')),
    # path('booking/', include('booking_portal.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
]
