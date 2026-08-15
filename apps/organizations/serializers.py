from rest_framework import serializers

from .models import Offer, Organization, OrganizationDocument


class CountrySerializer(serializers.ModelSerializer):
  """
  Serializer for a country, exposing its code and a localized display name.
  """

  name_fr = serializers.CharField(source="name", read_only=True)

  class Meta:
    model = Offer.country.field.related_model
    fields = ["code", "name_fr"]


class CauseSerializer(serializers.ModelSerializer):
  """
  Serializer for a cause (taxonomy) exposed on organizations and offers.
  """

  class Meta:
    model = Offer.causes.field.related_model
    fields = ["id", "name", "slug"]


class OfferOrganizationSummarySerializer(serializers.ModelSerializer):
  """
  Serializer for the compact organization summary embedded in an offer.
  """

  class Meta:
    model = Organization
    fields = [
      "id",
      "name",
      "slug",
      "type",
      "verification_status",
    ]


class OfferPreviewSerializer(serializers.ModelSerializer):
  """
  Serializer for offers rendered through MissionCard on the Org page.
  Mirrors the shape expected by the frontend OfferSummary/MissionCard.
  """

  organization = OfferOrganizationSummarySerializer(read_only=True)
  country = CountrySerializer(read_only=True)
  causes = CauseSerializer(many=True, read_only=True)

  class Meta:
    model = Offer
    fields = [
      "id",
      "slug",
      "title",
      "engagement_type",
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
    ]


class OrganizationDocumentSerializer(serializers.ModelSerializer):
  """
  Serializer for transparency documents shown on the Org page.
  """

  label = serializers.CharField(source="get_document_type_display")

  class Meta:
    model = OrganizationDocument
    fields = ["id", "label", "document_type", "file_url", "verified"]


class OrganizationSerializer(serializers.ModelSerializer):
  """
  Serializer for an organization's public profile.
  """

  country = CountrySerializer(read_only=True)
  causes = CauseSerializer(many=True, read_only=True)
  open_offers_count = serializers.IntegerField(read_only=True)

  offers = serializers.SerializerMethodField()
  documents = serializers.SerializerMethodField()

  class Meta:
    model = Organization
    fields = [
      "id",
      "name",
      "slug",
      "type",
      "country",
      "city",
      "registry_number",
      "size",
      "description",
      "mission",
      "website",
      "verification_status",
      "causes",
      "open_offers_count",
      "founded_year",
      "number_of_volunteers",
      "logo_url",
      "banner_url",
      "offers",
      "documents",
    ]

  def get_offers(self, obj):
    # Only fetch published offers.
    # We limit to 3 here to match the "Offres ouvertes (3)" preview,
    # or remove [:3] if you want to return all of them.
    published_offers = obj.offers.filter(status="published")[:3]
    return OfferPreviewSerializer(published_offers, many=True).data

  def get_documents(self, obj):
    documents = obj.documents.all()
    return OrganizationDocumentSerializer(documents, many=True).data
