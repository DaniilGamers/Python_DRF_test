from django_filters import rest_framework as filters


class AdFilter(filters.FilterSet):
    year_lt = filters.NumberFilter('year', 'lt')
    year_gt = filters.NumberFilter('year', 'gt')
    price_lt = filters.NumberFilter('price_original', 'lt')
    price_gt = filters.NumberFilter('price_original', 'gt')
    year_range = filters.RangeFilter('year')
    price_range = filters.RangeFilter('price_original')
    year_in = filters.BaseInFilter('year')
    price_in = filters.BaseInFilter('price_original')
    brand = filters.BaseInFilter('brand')
    order = filters.OrderingFilter(
        fields=(
            'brand',
            'price_original',
            ('id', 'asd')
        )
    )
