from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .enums import Role, Status


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


class CandidateRegistrationSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True, min_length=8)
  phone = serializers.CharField(required=False, allow_blank=True, max_length=20)

  def validate_email(self, value):
    User = get_user_model()
    if User.objects.filter(email__iexact=value).exists():
      raise serializers.ValidationError("Unable to register with this email.")
    return value

  def validate(self, data):
    validate_password(data["password"])
    return data

  def create(self, validated_data):
    User = get_user_model()
    user = User.objects.create_user(
      email=validated_data["email"],
      password=validated_data["password"],
      phone=validated_data.get("phone") or None,
      role=Role.CANDIDATE,
      status=Status.ACTIVE,
    )
    return user


class OrganizationRegistrationSerializer(serializers.Serializer):
  owner_email = serializers.EmailField()
  password = serializers.CharField(write_only=True, min_length=8)
  organization_name = serializers.CharField(max_length=180)
  organization_type = serializers.ChoiceField(
    choices=["association", "foundation", "ngo", "waqf"]
  )
  country_code = serializers.CharField(max_length=3)
  city = serializers.CharField(max_length=120)
  registry_number = serializers.CharField(max_length=120, allow_blank=True)
  description = serializers.CharField()
  mission = serializers.CharField(required=False, allow_blank=True)

  def validate_owner_email(self, value):
    User = get_user_model()
    if User.objects.filter(email__iexact=value).exists():
      raise serializers.ValidationError("Unable to register with this email.")
    return value

  def validate(self, data):
    validate_password(data["password"])
    return data
