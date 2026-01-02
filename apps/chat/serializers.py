from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "created_at"]


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    buyer_email = serializers.EmailField(source='buyer.email', read_only=True)
    seller_email = serializers.EmailField(source='seller.email', read_only=True)
    buyer_id = serializers.IntegerField(source='buyer.id', read_only=True)
    seller_id = serializers.IntegerField(source='seller.id', read_only=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "advertisement",
            "buyer",
            "seller",
            'buyer_id',
            'seller_id',
            'buyer_email',
            'seller_email',
            "created_at",
            "messages",
        )
        _read_only_fields = ('buyer_id', 'seller_id', 'buyer', 'seller')
