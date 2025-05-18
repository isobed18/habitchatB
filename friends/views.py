from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Friendship
from .serializers import FriendshipSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from habits.models import Habit

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Kullanıcı doğrulama
def send_friend_request(request):
    friend_username = request.data.get('friend_username')  # `friend_id` yerine `friend_username`
    try:
        friend = User.objects.get(username=friend_username)  # `id` yerine `username` ile arama
        if request.user == friend:
            return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Arkadaşlık isteği oluşturuluyor
        friendship, created = Friendship.objects.get_or_create(user=request.user, friend=friend, defaults={'status': 'pending'})
        if not created:
            return Response({'error': 'Friend request already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)
    
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friendship_id):
    try:
        friendship = Friendship.objects.get(id=friendship_id, friend=request.user, status='pending')
        friendship.accept()
        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
    except Friendship.DoesNotExist:
        return Response({'error': 'Friend request not found or already handled.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_friend_request(request, friendship_id):
    try:
        friendship = Friendship.objects.get(id=friendship_id, friend=request.user, status='pending')
        friendship.decline()
        return Response({'message': 'Friend request declined.'}, status=status.HTTP_200_OK)
    except Friendship.DoesNotExist:
        return Response({'error': 'Friend request not found or already handled.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_list(request):
    friends = Friendship.objects.filter(user=request.user, status='accepted').values('friend__username')  # `friend__id` yerine `friend__username`
    return Response(friends, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def requests_list(request):
    # Kullanıcının gelen arkadaşlık isteklerini al
    pending_requests = Friendship.objects.filter(friend=request.user, status='pending').values('user__username', 'id')
    return Response(pending_requests, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_habits_with_streaks(request):
    friend_username = request.query_params.get('friend_user')
    try:
        friend_user = User.objects.get(username=friend_username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    on_streak_habits = Habit.objects.filter(user=friend_user, streak__gt=0)
    habit_list = [
        {
            'id': habit.id,
            'name': habit.name,
            'habit_type': habit.habit_type,
            'target_count': habit.target_count,
            'target_time': habit.target_time,
            'total_time': str(habit.total_time) if habit.total_time else None,
            'completed_count': habit.completed_count, 
            'last_completed_date': habit.last_completed_date,  
            'streak': habit.streak,
            'count': habit.count,
            'frequency': habit.frequency,
        } for habit in on_streak_habits
    ]
    return Response({'habits': habit_list})
