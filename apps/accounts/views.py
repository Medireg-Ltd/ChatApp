from django.http import HttpResponse
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers import (
    LoginUserSerializer,
    LogoutSerializer,
    RegisterUserSerializer,
)

tags = ["Auth"]


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        # Add more rules here as needed
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


class RegisteruserView(APIView):
    serializer_class = RegisterUserSerializer

    @extend_schema(
        summary="Register User",
        description="""
            This endpoint registers a new user.
        """,
        tags=tags,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": "user registered succesfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class LoginUserView(APIView):
    serializer_class = LoginUserSerializer

    @extend_schema(
        summary="Login User",
        description="""
            This endpoint authenticates a user.
        """,
        tags=tags,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"success": "Login successful", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class LogoutUserAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout User",
        description="""
            This endpoint logs out a user.
        """,
        tags=tags,
        examples=[
            OpenApiExample(
                name="Logout user example",
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Logout Successful"})
