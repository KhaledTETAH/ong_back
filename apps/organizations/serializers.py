from rest_framework import serializers

from .models import Offer, Organization, OrganizationDocument


class OfferPreviewSerializer(serializers.ModelSerializer):
  """
  Lightweight serializer just for the cards on the Org page.
  """

  country = serializers.StringRelatedField()

  class Meta:
    model = Offer
    fields = [
      "id",
      "title",
      "slug",
      "city",
      "country",
      "duration_label",
      "engagement_type",
      "remote_mode",
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
  country = serializers.StringRelatedField()
  causes = serializers.StringRelatedField(many=True)

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
