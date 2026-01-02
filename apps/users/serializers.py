from django.db.transaction import atomic
from rest_framework import serializers
from apps.users.models import ProfileModel

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('user_id', 'name', 'surname', 'age')
        read_only_fields = ('user_id', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

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
            'is_client',
            'is_blocked',
            'created_at',
            'updated_at',
            'profile'

        )
        read_only_fields = ('user_id', 'is_active', 'is_staff', 'is_superuser', 'is_premium', 'created_at')
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


class UserStaffSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

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
            'is_client',
            'is_blocked',
            'created_at',
            'updated_at',
            'profile'

        )
        read_only_fields = (
        'user_id', 'is_active', 'is_staff', 'is_superuser', 'account_type', 'created_at')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_staff(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        return user
