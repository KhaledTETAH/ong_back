from rest_framework import serializers
from .enums import Role, Status
from .models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "email", "phone", "role", "status", "email_verified", "created_at"]
		read_only_fields = ["id", "role", "status", "email_verified", "created_at"]


class CandidateRegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)

	class Meta:
		model = User
		fields = ["id", "email", "phone", "password", "role", "status", "email_verified"]
		read_only_fields = ["id", "role", "status", "email_verified"]

	def create(self, validated_data):
		return User.objects.create_user(
			email=validated_data["email"],
			password=validated_data["password"],
			phone=validated_data.get("phone"),
			role=Role.CANDIDATE,
			status=Status.ACTIVE,
			email_verified=True,
		)


class OrganizationRegisterSerializer(serializers.Serializer):
	owner_email = serializers.EmailField()
	password = serializers.CharField(write_only=True, min_length=8)
	organization_name = serializers.CharField(max_length=180)
	organization_type = serializers.ChoiceField(choices=["association", "foundation", "ngo", "waqf"])
	country_code = serializers.CharField(max_length=2)
	city = serializers.CharField(max_length=120)
	registry_number = serializers.CharField(max_length=120)
	description = serializers.CharField()
	mission = serializers.CharField(required=False, allow_blank=True)

	def validate_owner_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError("A user with this email already exists.")
		return value

	def create(self, validated_data):
		from apps.engagement.models import Country, Organization

		country, _ = Country.objects.get_or_create(
			code=validated_data["country_code"].upper(),
			defaults={"name_fr": validated_data["country_code"].upper(), "is_covered": True},
		)
		user = User.objects.create_user(
			email=validated_data["owner_email"],
			password=validated_data["password"],
			role=Role.NGO_MEMBER,
			status=Status.ACTIVE,
			email_verified=True,
		)
		organization = Organization.objects.create(
			owner=user,
			name=validated_data["organization_name"],
			type=validated_data["organization_type"],
			country=country,
			city=validated_data["city"],
			registry_number=validated_data["registry_number"],
			description=validated_data["description"],
			mission=validated_data.get("mission", ""),
			verification_status="pending",
			is_active=True,
		)
		return {"user": user, "organization": organization}

class LogoutSerializer(serializers.Serializer):
	refresh = serializers.CharField(
		help_text="The refresh token to blacklist"
	)

	def validate_refresh(self, value):
		from rest_framework_simplejwt.tokens import RefreshToken
		from rest_framework_simplejwt.exceptions import TokenError

		try:
			RefreshToken(self.refresh)
		except TokenError:
			raise serializers.ValidationError("Token is invalid or already blacklisted")

		return value
