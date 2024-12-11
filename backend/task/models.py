from django.utils import timezone
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

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True, blank=False)
    description = models.TextField(max_length=512, null=True)
    status = models.CharField(choices=STATUS_CHOICES, blank=False, default=STATUS_CHOICES.get('new'))
    priority = models.CharField(choices=PRIORITY_CHOICES, blank=False,  default=PRIORITY_CHOICES.get('low'))
    created_at = models.DateTimeField(default=timezone.now())
    edited_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.author})'
