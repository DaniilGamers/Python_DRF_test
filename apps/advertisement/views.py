from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView)

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.permissions.is_super_user_permission import IsSuperUser
from core.permissions.is_seller import IsSeller

from apps.advertisement.models import AdvertisementModel

from apps.advertisement.serializers import AdvertisementSerializer, AdvertisementPhotoSerializer


class AdvertisementListView(ListAPIView):
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel
    permission_classes = (IsSeller,)


class AdvertisementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return (IsAuthenticated(),)
        return (IsSeller(),)


class AdvertisementAddPhotoView(UpdateAPIView):
    permission_classes = (IsSeller,)
    serializer_class = AdvertisementPhotoSerializer
    queryset = AdvertisementModel.objects.all()
    http_method_names = ('put',)

    def perform_update(self, serializer):
        ad = self.get_object()
        ad.photo.delete()
        super().perform_update(serializer)