from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from core.permissions.is_client import IsClient
from django.shortcuts import get_object_or_404

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from apps.advertisement.models import AdvertisementModel
from rest_framework.exceptions import PermissionDenied


class ChatCreateView(CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        ad = get_object_or_404(AdvertisementModel, id=self.request.data["advertisement"])

        if not getattr(self.request.user, 'is_client', False):
            raise PermissionDenied("Only the buyer can create a chat.")

        serializer.save(
            buyer=self.request.user,
            seller=ad.user,
            advertisement=ad
        )


class MessageCreateView(CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, id=self.kwargs["chat_id"])
        serializer.save(
            chat=chat,
            sender=self.request.user
        )


class ChatRetrieveView(RetrieveAPIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()
