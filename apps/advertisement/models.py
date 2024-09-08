from django.db import models

from core.services.file_service import FileService

from core.models import BaseModel
from apps.users.models import UserModel

from apps.users.models import ProfileModel


class AdvertisementModel(BaseModel):
    class Meta:
        db_table = 'advertisement'

    brand = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    year = models.IntegerField()
    photo = models.ImageField(upload_to=FileService.upload_car_photo, blank=True)
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, related_name='profile')