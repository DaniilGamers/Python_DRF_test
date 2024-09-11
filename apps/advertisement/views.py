from django.contrib.auth import get_user_model

from django.shortcuts import render


from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView)

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions.is_super_user_permission import IsSuperUser
from core.permissions.is_seller import IsSeller

from apps.advertisement.models import AdvertisementModel

from apps.advertisement.serializers import AdvertisementSerializer, AdvertisementPhotoSerializer

from apps.users.models import ProfileModel

UserModel = get_user_model()

BASIC_USER_AD_LIMIT = 5


class AdvertisementCreateListView(ListCreateAPIView):
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsSeller,)


class AdvertisementListView(ListAPIView):
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsSeller,)


class AdvertisementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return (IsSeller(),)
        return (IsSeller,), (IsSuperUser,)


class AdvertisementAddPhotoView(UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdvertisementPhotoSerializer
    queryset = AdvertisementModel.objects.all()
    http_method_names = ('put',)

    def perform_update(self, serializer):
        ad = self.get_object()
        ad.photo.delete()
        super().perform_update(serializer)