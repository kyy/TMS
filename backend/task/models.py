from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):

    STATUS_CHOICES = {
        'new': "новая",
        'open': "открытая",
        'completed': "завершена",
    }
    PRIORITY_CHOICES = {
        'low': "низкий",
        'middle': "средний",
        'high': "высокий",
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512, null=True)
    status = models.CharField(choices=STATUS_CHOICES, blank=False)
    priority = models.CharField(choices=PRIORITY_CHOICES, blank=False)
    created_at = models.DateField(default=datetime.now)
    edited_at = models.DateField(null=True)
    expires_at = models.DateField(null=True)