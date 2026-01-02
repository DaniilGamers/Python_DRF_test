from django.db import models
from datetime import timedelta
from django.utils import timezone
from core.services.currency import convert_to_uah
from django.db.models import Avg


class AdQuerySet(models.QuerySet):
    def less_than_year(self, year):
        return self.filter(year_lt=year)

    def more_than_year(self, year):
        return self.filter(year_gt=year)

    def higher_price(self, price):
        return self.filter(price_gt=price)

    def lower_price(self, price):
        return self.filter(price_lt=price)

    def only_brand(self, brand):
        return self.filter(brand=brand)


class AdManager(models.Manager):
    def get_queryset(self):
        return AdQuerySet(self.model)

    def less_than_year(self, year):
        return self.get_queryset().less_than_year(year)

    def more_than_year(self, year):
        return self.get_queryset().more_than_year(year)

    def more_price(self, price):
        return self.get_queryset().higher_price(price)

    def less_price(self, price):
        return self.get_queryset().lower_price(price)

    def only_brand(self, brand):
        return self.get_queryset().only_brand(brand)

    def recalc_views(self, ad):
        now = timezone.now()

        ad.viewed_total = ad.views.count()
        ad.viewed_in_day = ad.views.filter(
            timestamp__gte=now - timedelta(seconds=10)
        ).count()
        ad.viewed_in_week = ad.views.filter(
            timestamp__gte=now - timedelta(seconds=20)
        ).count()
        ad.viewed_in_month = ad.views.filter(
            timestamp__gte=now - timedelta(seconds=30)
        ).count()

        ad.save(
            update_fields=[
                "viewed_total",
                "viewed_in_day",
                "viewed_in_week",
                "viewed_in_month",
            ]
        )

    def prepare_price_fields(self, ad):
        price_uah, rate = convert_to_uah(
            ad.price_original,
            ad.currency
        )
        ad.price_uah = price_uah
        ad.rate_used = rate

    def avg_price_by_city(self, brand, model, city):
        return (
            self.filter(
                brand=brand,
                model=model,
                city=city,
                price_uah__isnull=False
            )
            .aggregate(avg=Avg("price_uah"))
            .get("avg")
        )

    def avg_price_ukraine(self, brand, model):
        return (
            self.filter(
                brand=brand,
                model=model,
                price_uah__isnull=False
            )
            .aggregate(avg=Avg("price_uah"))
            .get("avg")
        )
