from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.accounts.models import User


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]

    def validate(self, attrs):
        email = attrs.get("email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"error": "User with this Email already exists"}
            )

        return attrs

    def create(self, validated_data):
        # Remove the password from validated_data so it can be processed separately
        password = validated_data.pop("password")

        # Create the user instance without saving
        user = User(**validated_data)

        # Set and hash the user's password
        user.set_password(password)

        # Save the user instance
        user.save()

        return user


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30, min_length=8, write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "access_token",
            "refresh_token",
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(
                _("Authentication failed!. Credentials is invalid")
            )
        token = user.tokens()

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "access_token": str(token.get("access")),
            "refresh_token": str(token.get("refresh")),
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {"Bad token": ("token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return attrs

    def save(self, **Kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("Bad token")
