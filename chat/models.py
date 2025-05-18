from django.conf import settings
from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chatrooms")

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
