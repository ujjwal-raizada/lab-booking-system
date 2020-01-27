from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book-machine/<int:id>', views.book_machine, name='book-machine'),
    path('email/', views.email, name='email')
]