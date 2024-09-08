
from django.db import models

from core.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user2'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    ACCOUNT_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default='basic',
    )

    is_premium = models.BooleanField(default=False)

    def upgrade_to_premium(self):
        self.account_type = 'premium'
        self.is_premium = True
        self.save()


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ['id']

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.IntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')

