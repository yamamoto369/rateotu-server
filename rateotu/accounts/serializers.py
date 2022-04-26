from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomJwtTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.permission_role
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
