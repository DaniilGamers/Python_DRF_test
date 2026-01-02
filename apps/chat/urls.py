from django.urls import path
from .views import ChatCreateView, ChatRetrieveView, MessageCreateView

urlpatterns = [
    path('/', ChatCreateView.as_view(), name='chat-create'),
    path('/<int:pk>/', ChatRetrieveView.as_view(), name='chat-detail'),
    path('/<int:chat_id>/messages/', MessageCreateView.as_view(), name='message-create')
]
