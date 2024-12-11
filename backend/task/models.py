from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):

    STATUS_CHOICES = {
        True: "открытая",
        False: "завершена",
    }
    PRIORITY_CHOICES = {
        100: "низкий",
        500: "средний",
        900: "высокий",
    }

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True, blank=False)
    description = models.TextField(max_length=512, null=True)
    status = models.BooleanField(choices=STATUS_CHOICES, blank=False, default=True)
    priority = models.CharField(choices=PRIORITY_CHOICES, blank=False,  default=500)
    created_at = models.DateTimeField(default=timezone.now())
    edited_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    visibility = models.BooleanField(blank=False, default=True)

    def __str__(self) -> str:
        return self.name

