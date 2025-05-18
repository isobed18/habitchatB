from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

# Celery uygulamasını oluştur
app = Celery('habit_tracker')

# Ayarları Django settings.py'den al
app.config_from_object('django.conf:settings', namespace='CELERY')

# Projedeki tüm görevleri otomatik keşfet
app.autodiscover_tasks()

# Windows için multiprocessing hatasını önlemek adına
if os.name == 'nt':
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)

# Celery Beat için Database Scheduler kullan
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.timezone = 'Europe/Istanbul'
app.conf.enable_utc = False

# Varsayılan task rotası (Opsiyonel)
app.conf.task_routes = {
    'habit_tracker.tasks.add': {'queue': 'celery'},
}

# Varsayılan periyodik görev (Opsiyonel)
app.conf.beat_schedule = {
    'count-reset': {
        'task': 'habit_tracker.tasks.reset_habits_and_update_streak',
        'schedule': crontab(hour=23, minute=3),
    },
}

# Debug task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')