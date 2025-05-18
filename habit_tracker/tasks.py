from celery import Celery, shared_task
from datetime import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')
django.setup()
app = Celery('habit_tracker', broker='redis://localhost:6379', backend='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y


@shared_task
def reset_habits_and_update_streak():
    """
    Her gece çalışır, habit.count'u sıfırlar ve streak'i günceller.
    """
    print("count ve streak guncellendi log")
    from habits.models import Habit 
    habits = Habit.objects.all()
    for habit in habits:
        # Günlük sayacı sıfırla
        habit.count = 0
        
        # Streak'i güncelle
        habit.calculate_streak()
        
        # Değişiklikleri kaydet
        habit.save()
