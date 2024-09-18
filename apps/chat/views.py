from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.response import Response

from apps.chat.models import ChatRoom, Message
from apps.chat.serializers import ChatRoomSerializer, MessageSerializer

tags = ["Chat"]


@extend_schema(
    request=ChatRoomSerializer,
    responses={201: ChatRoomSerializer},
    summary="Create a new chatroom",
    tags=tags,
    description="Create a new chatroom and add it to the user's chatrooms.",
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_chatroom(request):
    serializer = ChatRoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: ChatRoomSerializer(many=True)},
    summary="View all chatrooms for the logged-in user",
    tags=tags,
    description="Retrieve a list of all chatrooms that the logged-in user is a member of.",
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_chatrooms(request):
    user = request.user
    chatrooms = ChatRoom.objects.filter(users=user)
    serializer = ChatRoomSerializer(chatrooms, many=True)
    return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="chatroom_id", type=int, location=OpenApiParameter.PATH, required=True
        )
    ],
    responses={200: MessageSerializer(many=True)},
    tags=tags,
    summary="See all messages within a given chatroom",
    description="Retrieve all messages from a specific chatroom.",
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_messages(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if chatroom not in request.user.chat_rooms.all():
        return Response(
            {"detail": "You do not have access to this chatroom."},
            status=status.HTTP_403_FORBIDDEN,
        )
    messages = Message.objects.filter(chat_room=chatroom).order_by("timestamp")
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="chatroom_id", type=int, location=OpenApiParameter.PATH, required=True
        )
    ],
    tags=tags,
    request=MessageSerializer,
    responses={201: MessageSerializer},
    summary="Send a message to a given chatroom",
    description="Send a message to a specific chatroom.",
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def send_message(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if chatroom not in request.user.chat_rooms.all():
        return Response(
            {"detail": "You do not have access to this chatroom."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(chat_room=chatroom, sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="message_id", type=int, location=OpenApiParameter.PATH, required=True
        )
    ],
    tags=tags,
    responses={204: OpenApiResponse(description="Message deleted successfully")},
    summary="Delete a message",
    description="Delete a specific message from the chatroom.",
)
@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.sender != request.user:
        return Response(
            {"detail": "You do not have permission to delete this message."},
            status=status.HTTP_403_FORBIDDEN,
        )
    message.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="chatroom_id", type=int, location=OpenApiParameter.PATH, required=True
        )
    ],
    tags=tags,
    responses={204: OpenApiResponse(description="Chatroom deleted successfully")},
    summary="Delete a chatroom",
    description="Delete a specific chatroom.",
)
@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if chatroom not in request.user.chat_rooms.all():
        return Response(
            {"detail": "You do not have permission to delete this chatroom."},
            status=status.HTTP_403_FORBIDDEN,
        )
    chatroom.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="chatroom_id", type=int, location=OpenApiParameter.PATH, required=True
        )
    ],
    tags=tags,
    request=ChatRoomSerializer,
    responses={200: ChatRoomSerializer},
    summary="Rename a chatroom",
    description="Rename a specific chatroom.",
)
@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def rename_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if chatroom not in request.user.chat_rooms.all():
        return Response(
            {"detail": "You do not have permission to rename this chatroom."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ChatRoomSerializer(chatroom, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
