from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "email"]
    read_only_fields = ["id", "email"]


class LogoutSerializer(serializers.Serializer):
  refresh = serializers.CharField(help_text="The refresh token to blacklist")

  def validate_refresh(self, value):
    from rest_framework_simplejwt.exceptions import TokenError
    from rest_framework_simplejwt.tokens import RefreshToken

    try:
      RefreshToken(self.refresh)
    except TokenError:
      raise serializers.ValidationError("Token is invalid or already blacklisted")

    return value
