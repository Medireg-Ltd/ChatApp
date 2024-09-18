from rest_framework import serializers

from apps.chat.models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["id", "name", "users"]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    chat_room = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ["id", "sender", "recipient", "chat_room", "content", "timestamp"]
