from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.api_register_view, name='api_register'),
    path('login/', views.api_user_login, name='api_login'),
    path('get_server_time/', views.api_get_server_time, name='api_get_server_time'),
]