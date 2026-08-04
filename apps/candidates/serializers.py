from rest_framework import serializers

from apps.core.models import Cause, Country, Skill

from .models import CandidateProfile, DesiredPosition
from .validators import validate_desired_position


class DesiredPositionSerializer(serializers.ModelSerializer):
  """
  Serializer for the 'Desired Position' profile.
  Handles M2M fields by accepting/returning lists of UUIDs.
  """

  # M2M fields: Accepts and returns lists of UUIDs
  preferred_causes = serializers.PrimaryKeyRelatedField(
    queryset=Cause.objects.all(), many=True, required=False
  )
  excluded_causes = serializers.PrimaryKeyRelatedField(
    queryset=Cause.objects.all(), many=True, required=False
  )
  preferred_countries = serializers.PrimaryKeyRelatedField(
    queryset=Country.objects.all(), many=True, required=False
  )
  skills_to_leverage = serializers.PrimaryKeyRelatedField(
    queryset=Skill.objects.all(), many=True, required=False
  )
  skills_to_develop = serializers.PrimaryKeyRelatedField(
    queryset=Skill.objects.all(), many=True, required=False
  )

  class Meta:
    model = DesiredPosition
    fields = [
      "id",
      "engagement_types",
      "preferred_causes",
      "excluded_causes",
      "modalities",
      "availability",
      "mobility",
      "position_level",
      "preferred_countries",
      "preferred_regions",
      "skills_to_leverage",
      "skills_to_develop",
      "min_daily_rate",
      "available_from",
      "available_until",
    ]

  def validate(self, data):
    validate_desired_position(data)
    return data


class ActivelyLookingSerializer(serializers.ModelSerializer):
  """
  Lightweight serializer just for the "Actively Looking" toggle.
  """

  class Meta:
    model = CandidateProfile
    fields = ["actively_looking"]
