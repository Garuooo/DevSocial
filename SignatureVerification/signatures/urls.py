

from django.urls import path
from . import views
urlpatterns = [
    path('', views.signatures, name='signatures'),
    path('signature/<str:pk>', views.signature, name='signature'),
    path('create-signature/', views.create_signature, name='create_signature'),
    path('update-signature/<str:pk>',
         views.update_signature, name='update_signature'),
    path('delete-signature/<str:pk>',
         views.delete_signature, name='delete_signature'),
    path('verify-two-signatures/', views.verify_two_signatures,
         name='verify_two_signatures'),
    path('create-note/<str:pk>', views.create_note, name='create_note'),
    path('update-note/<str:pk>', views.update_note, name='update_note'),
    path('delete-note/<str:pk>', views.delete_note, name='delete_note'),
]
