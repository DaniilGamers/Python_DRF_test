from rest_framework import serializers

from apps.advertisement.models import AdvertisementModel


class AdvertisementSerializer(serializers.ModelSerializer):
    viewed_in_day = serializers.IntegerField(read_only=True)
    viewed_in_week = serializers.IntegerField(read_only=True)
    viewed_in_month = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdvertisementModel
        fields = ('id', 'user_id', 'brand',  'model', 'description', 'price_original', 'currency', 'viewed_in_day', 'viewed_in_week', 'viewed_in_month', 'price_uah', 'average_price_in_cities', 'average_price_in_ukraine', 'year', 'photo', 'photo_file', 'city', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user_id', 'viewed_total', 'viewed_in_day', 'viewed_in_month', 'viewed_in_week', 'photo', 'timestamp', 'price_uah', 'rate_used', 'created_at')

    extra_kwargs = {'photo': {'required': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return data

        user = request.user

        if user.is_basic:
            stats_fields = [
                "viewed_total",
                "viewed_in_day",
                "viewed_in_week",
                "viewed_in_month",
                "average_price_in_cities",
                "average_price_in_ukraine",
            ]
            for field in stats_fields:
                data.pop(field, None)

        return data


class AdvertisementPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementModel
        fields = ('photo',)
        extra_kwargs = {'photo': {'required': True}}
