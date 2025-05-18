from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.get_habits, name='api_get_habits'),
    path('add/', views.add_habit, name='api_add_habit'),
    path('update/<int:habit_id>/', views.update_habit, name='api_update_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='api_delete_habit'),
]
