from __future__ import absolute_import, unicode_literals

# Celery uygulamasını projenin geri kalanına tanıt
from .my_celery import app as celery_app

__all__ = ('celery_app',)
