from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_habit_view, name='add_habit'),
    path('increment/<int:habit_id>/', views.increment_habit, name='increment_habit'),
]
