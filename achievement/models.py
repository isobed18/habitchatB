from django.db import models
from django.contrib.auth import get_user_model
from challange.models import Challenge
class Achievement(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_awarded = models.DateTimeField(auto_now_add=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='achievements')

