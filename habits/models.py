from django.db import models
from django.contrib.auth import get_user_model
from datetime import date, timedelta

class Habit(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)

    # Alışkanlık tipi: Zaman kontrollü veya sayım kontrollü
    habit_type = models.CharField(max_length=10, choices=[('time', 'Time-based'), ('count', 'Count-based')])


    

    # Kullanıcı istatistikleri
    streak = models.IntegerField(default=0)  # Kesintisiz başarı serisi
    count = models.PositiveIntegerField(default=0)  # Mevcut sayım
    total_time = models.DurationField(null=True, blank=True)  # Toplam süre (zaman kontrollü)
    last_completed_date = models.DateField( null=True, blank=True)  # Son tamamlanma tarihi
    completion_dates = models.JSONField(default=list)  # Tamamlanan tarihleri saklamak için
    completed_count = models.IntegerField(default=0)  # Tamamlanan toplam gün sayısı

    # Hedefler
    target_count = models.IntegerField(null=True, blank=True)  
    target_time = models.DurationField(null=True, blank=True)  # Zaman kontrollü için hedef süre

    # Sıklık
    FREQUENCY_CHOICES = [
        ('daily', 'Günlük'),
        ('weekly', 'Haftalık'),
        ('monthly', 'Aylık'),
    ]
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)

    

    def calculate_completed_count(self):
        completed_count = len(self.completion_dates)
        return completed_count

    def calculate_streak(self):
        """Tamamlanma tarihine göre streak hesaplar."""
        today = date.today() # Bugünü string formatında al
        streak = 0
        for i in range(len(self.completion_dates) - 1, -1, -1):
            if self.completion_dates[i] == (today - timedelta(days=streak)).isoformat():  # String formatında karşılaştır
                streak += 1
            else:
                break
        self.streak = streak
        return streak

    def __str__(self):  
        return self.name
