from rest_framework import serializers
from .models import Organization, Offer

class OfferPreviewSerializer(serializers.ModelSerializer):
	"""
  Lightweight serializer just for the cards on the Org page.
  """
	country = serializers.StringRelatedField()
	
	class Meta:
		model = Offer
		fields = [
			'id', 'title', 'slug', 'city', 'country', 
			'duration_label', 'engagement_type', 'remote_mode'
		]

class OrganizationSerializer(serializers.ModelSerializer):
	country = serializers.StringRelatedField()
	causes = serializers.StringRelatedField(many=True)
	

	offers = serializers.SerializerMethodField()

	class Meta:
		model = Organization
		fields = [
			'id', 'name', 'slug', 'type', 'country', 'city', 
			'registry_number', 'size', 'description', 'mission', 
			'website', 'verification_status', 'causes', 'founded_year', 
			'logo_url', 'banner_url', 'offers'
		]

	def get_offers(self, obj):
		# Only fetch published offers. 
		# We limit to 3 here to match the "Offres ouvertes (3)" preview, 
		# or remove [:3] if you want to return all of them.
		published_offers = obj.offers.filter(status='published')[:3]
		return OfferPreviewSerializer(published_offers, many=True).data