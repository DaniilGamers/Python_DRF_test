from django.db import models

from core.services.file_service import FileService

from django.core import validators as V

from core.models import BaseModel

from apps.users.models import ProfileModel, UserModel


class AdvertisementModel(BaseModel):
    class Meta:
        db_table = 'advertisement'
        ordering = ('-id',)

    brand = models.CharField(max_length=10, validators=(V.MinLengthValidator(2),))
    model = models.CharField(max_length=10, validators=(V.MinLengthValidator(2),))
    description = models.CharField(max_length=100, validators=(V.MinLengthValidator(10),))
    price = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(1_000_000)))
    year = models.IntegerField(validators=(V.MinValueValidator(1990), V.MaxValueValidator(2010)))
    photo = models.ImageField(upload_to=FileService.upload_car_photo, blank=True)

    MONEY_CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('UAH', 'UAH'),
        ('EUR', 'EUR  ')
    ]

    money_currency = models.CharField(max_length=10, choices=MONEY_CURRENCY_CHOICES, blank=False)
    user = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='advertisement')

