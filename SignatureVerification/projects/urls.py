from django.urls import path
from . import views
urlpatterns = [
    path("projects/", views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('create-project/', views.create_project, name='create_project'),
    path('update-project/<str:pk>/', views.update_project, name='update_project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete_project'),
    path('update-review/<str:pk>/', views.update_review, name='update_review'),
    path('delete-review/<str:pk>/', views.delete_review, name='delete_review'),
]
