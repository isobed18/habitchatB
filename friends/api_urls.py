from django.urls import path
from . import views

urlpatterns = [
    path('send_request/', views.send_friend_request, name='api_send_friend_request'),
    path('accept/<int:friendship_id>/', views.accept_friend_request, name='api_accept_friend_request'),
    path('decline/<int:friendship_id>/', views.decline_friend_request, name='api_decline_friend_request'),
    path('list/', views.friend_list, name='api_friend_list'),
    path('requests_list/', views.requests_list, name='api_requests_list'),
    path('get_habits_with_streaks/', views.get_habits_with_streaks, name='api_get_habits_with_streaks'),

]
