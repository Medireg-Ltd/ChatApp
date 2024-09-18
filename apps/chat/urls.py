from django.urls import path

from . import views

urlpatterns = [
    path("chatroom/create/", views.create_chatroom, name="create_chatroom"),
    path("chatroom/", views.list_chatrooms, name="list_chatrooms"),
    path(
        "chatroom/<int:chatroom_id>/messages/",
        views.list_messages,
        name="list_messages",
    ),
    path("chatroom/<int:chatroom_id>/send/", views.send_message, name="send_message"),
    path(
        "message/<int:message_id>/delete/", views.delete_message, name="delete_message"
    ),
    path(
        "chatroom/<int:chatroom_id>/delete/",
        views.delete_chatroom,
        name="delete_chatroom",
    ),
    path(
        "chatroom/<int:chatroom_id>/rename/",
        views.rename_chatroom,
        name="rename_chatroom",
    ),
]
