from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    groups = models.ManyToManyField('groups.Group', related_name='user_groups')
