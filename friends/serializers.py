from rest_framework import serializers
from .models import Friendship

class FriendshipSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    friend = serializers.CharField(source='friend.username', read_only=True)  # `friend` alanı username döndürüyor

    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

