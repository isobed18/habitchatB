from django.db import models
from django.contrib.auth import get_user_model

class Friendship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='friendships_initiated')
    friend = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='friendships_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def accept(self):
        """Accept the friendship request."""
        self.status = 'accepted'
        self.save()
        # Ensure a reciprocal relationship
        Friendship.objects.get_or_create(user=self.friend, friend=self.user, defaults={'status': 'accepted'})

    def decline(self):
        """Decline the friendship request."""
        self.delete()
