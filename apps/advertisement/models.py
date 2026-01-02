import os
from django.db import models

from core.services.file_service import FileService


from django.core import validators as V

from core.models import BaseModel

from apps.users.models import UserModel

from apps.advertisement.managers import AdManager


class AdvertisementModel(BaseModel):
    class Meta:
        db_table = 'advertisement'
        ordering = ('-id',)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('needs_edit', 'Needs Edit')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    edit_attempts = models.PositiveIntegerField(default=0)

    class Brand(models.TextChoices):
        BMW = "BMW"
        mercedes = "Mercedes"
        ferrari = "Ferrari"
        toyota = "Toyota"
        audi = "Audi"

    brand = models.CharField(max_length=10, choices=Brand.choices, blank=False)
    model = models.CharField(max_length=10, validators=(V.MinLengthValidator(2),), blank=False)
    description = models.CharField(max_length=100, validators=(V.MinLengthValidator(10),))
    price_original = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(1_000_000)))
    rate_used = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_uah = models.PositiveIntegerField(null=True, blank=True)
    year = models.IntegerField(validators=(V.MinValueValidator(1990), V.MaxValueValidator(2010)))
    photo_file = models.ImageField(upload_to=FileService.upload_car_photo)
    photo = models.CharField(max_length=255, blank=True, editable=False)

    class Currency(models.TextChoices):
        USD = "USD"
        EUR = "EUR"
        UAH = "UAH"

    currency = models.CharField(max_length=10, choices=Currency.choices, blank=False)
    city = models.CharField(max_length=20, validators=(V.MinLengthValidator(3),))
    viewed_total = models.IntegerField(default=0)
    viewed_in_day = models.IntegerField(default=0)
    viewed_in_week = models.IntegerField(default=0)
    viewed_in_month = models.IntegerField(default=0)
    average_price_in_cities = models.IntegerField(default=0, null=True, blank=True)
    average_price_in_ukraine = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='advertisement')
    timestamp = models.DateTimeField(auto_now_add=True)

    currency_rates = {
        "USD": 38,
        "EUR": 41,
        "UAH": 1
    }

    created_at = models.DateTimeField(auto_now_add=True)

    objects = AdManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the file first
        if self.photo_file:
            file_name = os.path.basename(self.photo_file.name)
            if self.photo != file_name:
                self.photo = file_name
                super().save(update_fields=['photo'])


class AdvertisementView(models.Model):
    ad = models.ForeignKey(AdvertisementModel, on_delete=models.CASCADE, related_name='views')
    timestamp = models.DateTimeField(auto_now_add=True)
