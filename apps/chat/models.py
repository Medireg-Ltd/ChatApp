from apps.accounts.models import User
from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="chat_rooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, null=True, blank=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.sender} to {self.recipient or self.chat_room}: {self.content[:20]}"
        )
