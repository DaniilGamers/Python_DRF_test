from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.generics import (GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView)

from rest_framework.permissions import AllowAny

from core.permissions.is_super_user_permission import IsSuperUser

from core.permissions.is_seller import IsSeller, IsSellerOrStaffOrAdmin

from apps.advertisement.models import AdvertisementModel, AdvertisementView

from apps.advertisement.serializers import AdvertisementSerializer, AdvertisementPhotoSerializer

from rest_framework.response import Response

from core.services.text_checker import check_bad_words

from core.services.notification_service import notify_manager

from rest_framework.exceptions import ValidationError

from .filter import AdFilter

UserModel = get_user_model()

BASIC_USER_AD_LIMIT = 1


class AdvertisementCreateListView(ListCreateAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = (IsSeller,)

    def get_queryset(self):
        return AdvertisementModel.objects.with_auto_counts()

    def perform_create(self, serializer):

        user = self.request.user

        if user.is_basic:
            if AdvertisementModel.objects.filter(user=user).count() >= 1:

                raise ValidationError("Basic users can only post one ad.")

        ad = serializer.save(
            user=self.request.user
        )

        if check_bad_words(ad.description):
            ad.status = 'needs_edit'
        else:
            ad.status = 'active'

        ad.save(update_fields=['status'])

        AdvertisementModel.objects.prepare_price_fields(ad)

        ad.save()

        if check_bad_words(ad.description):
            print("Has foul language. Fix it right away!")
            raise ValidationError("Has foul language. Fix it right away!")


class AdvertisementListView(ListAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)
    queryset = AdvertisementModel.objects.all()
    filterset_class = AdFilter


class AdvertisementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return (IsSellerOrStaffOrAdmin(),)
        if self.request.method == 'GET':
            return (IsSeller(),)
        if self.request.method == 'PATCH':
            return (IsSeller(),)
        return (IsSeller,), (IsSuperUser,)

    def retrieve(self, request, *args, **kwargs):
        ad = self.get_object()

        AdvertisementView.objects.create(ad=ad)
        AdvertisementModel.objects.recalc_views(ad)

        avg_city = AdvertisementModel.objects.avg_price_by_city(
            brand=ad.brand,
            model=ad.model,
            city=ad.city
        )

        avg_ukraine = AdvertisementModel.objects.avg_price_ukraine(
            brand=ad.brand,
            model=ad.model
        )

        response = super().retrieve(request, *args, **kwargs)

        if request.user.is_premium:
            response.data["average_price_in_cities"] = avg_city
            response.data["average_price_in_ukraine"] = avg_ukraine
        else:
            response.data.pop("average_price_in_cities", None)
            response.data.pop("average_price_in_ukraine", None)

        return response

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)

        ad = self.get_object()

        if ad.edit_attempts >= 3:
            print("became inactive moron")
        else:
            print("it's inactive idiot")
        return response

    def perform_update(self, serializer):
        ad = serializer.save()

        ad.edit_attempts += 1

        if check_bad_words(ad.description):
            if ad.edit_attempts >= 3:
                notify_manager(ad)
                ad.status = 'inactive'

            else:
                ad.status = 'needs_edit'
        else:
            if ad.status != 'inactive':
                ad.status = 'active'
                ad.edit_attempts = 0

        ad.save(update_fields=['status', 'edit_attempts'])

        if ad.edit_attempts >= 3:
            raise ValidationError("Unfortunately you didn't remove foul language. The ad became inactive")

        if check_bad_words(ad.description):
            raise ValidationError("It still has foul language. Try edit again")


class AdvertisementAddPhotoView(UpdateAPIView):
    permission_classes = (IsSeller,)
    serializer_class = AdvertisementPhotoSerializer
    queryset = AdvertisementModel.objects.all()
    http_method_names = ('put',)

    def perform_update(self, serializer):
        ad = self.get_object()
        ad.photo.delete()
        super().perform_update(serializer)


class AdvertisementViewerView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()

    def put(self, request, *args, **kwargs):
        ad = self.get_object()
        ad.viewed_total += 1
        ad.viewed_in_day += 1
        ad.viewed_in_week += 1
        ad.viewed_in_month += 1

        ad.save()

        serializer = AdvertisementSerializer(ad)
        return Response(serializer.data, status.HTTP_200_OK)
