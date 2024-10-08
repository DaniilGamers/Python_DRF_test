from rest_framework import serializers

from apps.advertisement.models import AdvertisementModel


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementModel
        fields = ('id', 'brand',  'model', 'description', 'price', 'money_currency', 'year', 'photo', 'created_at', 'updated_at')


class AdvertisementPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementModel
        fields = ('photo',)
        extra_kwargs = {'photo': {'required': True}}
