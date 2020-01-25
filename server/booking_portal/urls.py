from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book-machine', views.book_machine, name='book-machine')
]