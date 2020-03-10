from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book-machine/<int:id>', views.book_machine, name='book-machine'),
    path('email/', views.email, name='email'),
    path('instrument-list/', views.instrument_list, name='instrument-list'),
    path('view-slots/', views.slot_list, name='slot-list'),
    path('faculty/', views.faculty_portal, name='faculty_portal'),
    path('requests_faculty/accept/<int:id>', views.faculty_request_accept, name='faculty_request_accept'),
    path('requests_faculty/reject/<int:id>', views.faculty_request_reject, name='faculty_request_reject'),
    path('lab-assistant/', views.lab_assistant_portal, name='lab_assistant'),
    path('requests_assistant/accept/<int:id>', views.lab_assistant_accept, name='faculty_request_accept'),
    path('requests_assistant/reject/<int:id>', views.lab_assistant_reject, name='faculty_request_reject'),
]
