from django_filters import rest_framework as filters

from apps.advertisement.models import AdvertisementModel


class AdFilter(filters.FilterSet):
    year_gtd = filters.NumberFilter('year', 'lt')
    year_range = filters.RangeFilter('year')
    year_in = filters.BaseInFilter('year')
    order = filters.OrderingFilter(
        fields=(
            'brand',
            'price',
            ('id', 'asd')
        )
    )