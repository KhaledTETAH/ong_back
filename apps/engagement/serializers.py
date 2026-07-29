import hashlib
import secrets

from django.utils import timezone
from rest_framework import serializers

from .models import (
	Application,
	Cause,
	Country,
	Language,
	Offer,
	Organization,
	SavedOffer,
	Skill,
	SponsorshipMission,
)


class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Country
		fields = ["code", "name_fr"]


class CauseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cause
		fields = ["id", "name", "slug"]


class SkillSerializer(serializers.ModelSerializer):
	class Meta:
		model = Skill
		fields = ["id", "name", "slug"]


class LanguageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Language
		fields = ["code", "name_fr"]


class OrganizationSummarySerializer(serializers.ModelSerializer):
	country = CountrySerializer()
	causes = CauseSerializer(many=True)
	open_offers_count = serializers.IntegerField(read_only=True)

	class Meta:
		model = Organization
		fields = [
			"id",
			"name",
			"slug",
			"type",
			"country",
			"city",
			"description",
			"verification_status",
			"open_offers_count",
			"causes",
		]


class OfferSummarySerializer(serializers.ModelSerializer):
	organization = OrganizationSummarySerializer()
	country = CountrySerializer()
	causes = CauseSerializer(many=True)
	languages = LanguageSerializer(many=True)
	skills = SkillSerializer(many=True)

	class Meta:
		model = Offer
		fields = [
			"id",
			"slug",
			"title",
			"engagement_type",
			"employment_contract",
			"country",
			"city",
			"region",
			"remote_mode",
			"duration_label",
			"duration_days",
			"experience_level",
			"featured",
			"published_at",
			"organization",
			"causes",
			"languages",
			"skills",
		]


class OfferDetailSerializer(OfferSummarySerializer):
	is_saved = serializers.SerializerMethodField()
	has_applied = serializers.SerializerMethodField()

	class Meta(OfferSummarySerializer.Meta):
		fields = OfferSummarySerializer.Meta.fields + [
			"description",
			"responsibilities",
			"desired_profile",
			"conditions",
			"expires_at",
			"views_count",
			"is_saved",
			"has_applied",
		]

	def get_is_saved(self, obj):
		user = self.context["request"].user
		return bool(user.is_authenticated and SavedOffer.objects.filter(user=user, offer=obj).exists())

	def get_has_applied(self, obj):
		user = self.context["request"].user
		return bool(user.is_authenticated and Application.objects.filter(candidate=user, offer=obj).exists())


class OrganizationDetailSerializer(OrganizationSummarySerializer):
	offers = OfferSummarySerializer(many=True)

	class Meta(OrganizationSummarySerializer.Meta):
		fields = OrganizationSummarySerializer.Meta.fields + ["registry_number", "size", "mission", "website", "offers"]


class ApplicationSerializer(serializers.Serializer):
	cover_letter = serializers.CharField(required=False, allow_blank=True, max_length=10000)

	def create(self, validated_data):
		request = self.context["request"]
		offer = self.context["offer"]
		application, _ = Application.objects.get_or_create(
			offer=offer,
			candidate=request.user,
			defaults={"cover_letter": validated_data.get("cover_letter", "")},
		)
		return application


class ShareOfferSerializer(serializers.Serializer):
	channel = serializers.ChoiceField(choices=["copy_link", "email", "linkedin", "facebook", "whatsapp", "other"])


class SponsorshipMissionSerializer(serializers.ModelSerializer):
	country_code = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=2)
	cause_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
	consent = serializers.BooleanField(write_only=True)
	website = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
	debug_verification_token = serializers.CharField(read_only=True)

	class Meta:
		model = SponsorshipMission
		fields = [
			"tracking_uuid",
			"contact_email",
			"company_name",
			"company_legal_id",
			"country_code",
			"region",
			"title",
			"description",
			"objectives",
			"deliverables",
			"required_profiles",
			"man_days",
			"visibility",
			"status",
			"verified_email_at",
			"cause_ids",
			"consent",
			"website",
			"debug_verification_token",
			"created_at",
		]
		read_only_fields = ["tracking_uuid", "status", "verified_email_at", "created_at"]

	def validate_website(self, value):
		if value:
			raise serializers.ValidationError("Submission rejected.")
		return value

	def validate_consent(self, value):
		if not value:
			raise serializers.ValidationError("Consent is required.")
		return value

	def create(self, validated_data):
		cause_ids = validated_data.pop("cause_ids", [])
		validated_data.pop("consent", None)
		validated_data.pop("website", None)
		country_code = validated_data.pop("country_code", "")
		country = None
		if country_code:
			country, _ = Country.objects.get_or_create(
				code=country_code.upper(),
				defaults={"name_fr": country_code.upper(), "is_covered": True},
			)
		token = secrets.token_urlsafe(48)
		mission = SponsorshipMission.objects.create(
			**validated_data,
			country=country,
			verification_token_hash=hashlib.sha256(token.encode("utf-8")).hexdigest(),
		)
		if cause_ids:
			mission.causes.set(Cause.objects.filter(id__in=cause_ids))
		mission.debug_verification_token = token
		return mission


class SponsorshipMissionReadSerializer(serializers.ModelSerializer):
	country_code = serializers.CharField(source="country.code", allow_null=True)
	causes = CauseSerializer(many=True)

	class Meta:
		model = SponsorshipMission
		fields = [
			"tracking_uuid",
			"contact_email",
			"company_name",
			"company_legal_id",
			"country_code",
			"region",
			"title",
			"description",
			"objectives",
			"deliverables",
			"required_profiles",
			"man_days",
			"visibility",
			"status",
			"verified_email_at",
			"causes",
			"created_at",
		]
