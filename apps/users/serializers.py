from django.db.transaction import atomic
from rest_framework import serializers
from apps.users.models import ProfileModel

from django.contrib.auth import get_user_model

from apps.advertisement.serializers import AdvertisementSerializer

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(many=True)
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'created_at', 'updated_at', 'advertisement',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(),

    class Meta:

        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_basic',
            'is_premium',
            'is_seller',
            'last_login',
            'created_at',
            'updated_at',
            'profile',

        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'account_type', 'is_seller', 'last_login', 'created_at')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        return user
