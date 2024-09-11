
from django.db import models

from core.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

from apps.users.managers import UserManager




class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel,):
    class Meta:
        db_table = 'auth_user2'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    ACCOUNT_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    is_premium = models.BooleanField(default=False)

    is_basic = models.BooleanField(default=False)


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ['id']

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.IntegerField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='profile')