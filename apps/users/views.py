from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.generics import GenericAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from rest_framework.response import Response

from core.permissions.is_seller import IsSeller, IsAdminSuper

from core.permissions.is_staff_or_admin import IsStaffOrAdmin

from apps.users.serializers import UserSerializer, UserStaffSerializer

from core.services.payment_service import PaymentService, PREMIUM_PRICE
UserModel = get_user_model()


class UserListCreateView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)


class UserToClientView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_seller:
            return Response('The user is already decided to be seller')

        if not user.is_client:
            user.is_client = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToSellerView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_client:
            return Response('The user is already decided to be buyer')

        if not user.is_seller:
            user.is_seller = True
            user.save()

        if not user.is_basic:
            user.is_basic = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserBlockView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStaffOrAdmin)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can block or unblock users"},
                status=status.HTTP_403_FORBIDDEN
            )

        if not user.is_blocked:
            user.is_blocked = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserUnBlockView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsStaffOrAdmin)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can block or unblock users"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user.is_blocked:
            user.is_blocked = False
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BuyPremiumView(GenericAPIView):
    permission_classes = (IsSeller,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def post(self, request):
        user = request.user
        provider = request.data.get("provider")
        force_fail = request.data.get("force_fail")

        if user.is_premium:
            return Response({"detail": "Already premium"}, status=400)

        if provider not in ["paypal", "privatbank"]:
            return Response({"detail": "Invalid provider"}, status=400)

        payment, status_payment = PaymentService.process_payment(user, provider, force_fail)

        if status_payment != "SUCCESS":
            return Response({
                "detail": "Payment failed.",
                "transaction_id": payment.transaction_id,
                "provider": provider,
                "price": payment.amount
            }, status=400)

        # Activate premium only on success
        user.is_premium = True
        user.is_basic = False
        user.save()

        return Response({
            "detail": "Premium purchased successfully (mock).",
            "transaction_id": payment.transaction_id,
            "price": PREMIUM_PRICE,
            "provider": provider
        }, status=200)


class UserStaffCreateView(ListCreateAPIView):
    permission_classes = (IsAdminSuper,)
    queryset = UserModel.objects.all()
    serializer_class = UserStaffSerializer


