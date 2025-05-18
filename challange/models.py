from django.db import models
from habits.models import Habit
class Challenge(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='challenges')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target_days = models.IntegerField()
    is_completed = models.BooleanField(default=False)

