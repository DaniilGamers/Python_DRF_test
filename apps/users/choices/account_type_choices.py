from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default='basic',
    )