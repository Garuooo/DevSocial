from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path("login/", views.log_in, name="login"),
    path("login-with-signature", views.login_with_signature,
         name='login_with_signature'),
    path("logout/", views.log_out, name="logout"),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('profile/history/', views.history, name='history'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('create-skill/', views.create_skill, name='create_skill'),
    path('edit-skill/<str:pk>/', views.edit_skill, name='edit_skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete_skill'),
    path("inbox/",views.all_messages,name="inbox"),
    path("message/<str:id>",views.view_message,name="message"),
    path("send-message/<str:pk>/",views.create_message,name="create_message")
]
