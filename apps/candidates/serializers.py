from rest_framework import serializers

from apps.core.models import Cause, Country, Skill

from .models import Application, CandidateProfile, DesiredPosition
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
  preferred_geographies = serializers.PrimaryKeyRelatedField(
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
      "position_title",
      "engagement_types",
      "preferred_causes",
      "excluded_causes",
      "modalities",
      "availability",
      "mobility",
      "position_level",
      "preferred_geographies",
      "skills_to_leverage",
      "skills_to_develop",
      "min_daily_rate",
      "available_from",
      "available_until",
      "email_alerts",
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


class ApplicationSerializer(serializers.ModelSerializer):
  """
  Serializer for an application in the candidate dashboard.
  """

  TRACKER_STAGES = ["submitted", "prequalified", "interview", "decision", "offer"]

  offer = serializers.CharField(source="offer.title", read_only=True)
  org = serializers.CharField(source="offer.organization.name", read_only=True)
  engagement_type = serializers.CharField(
    source="offer.get_engagement_type_display", read_only=True
  )
  location = serializers.SerializerMethodField()
  submitted_at = serializers.DateTimeField(
    source="created_at", format="%Y-%m-%d", read_only=True
  )
  tracker = serializers.SerializerMethodField()

  class Meta:
    model = Application
    fields = [
      "id",
      "offer",
      "org",
      "engagement_type",
      "stage",
      "location",
      "submitted_at",
      "updated_at",
      "tracker",
    ]

  def get_location(self, obj):
    if obj.offer.city:
      return obj.offer.city
    return obj.offer.country.name if obj.offer.country else None

  def get_tracker(self, obj):
    current_index = (
      self.TRACKER_STAGES.index(obj.stage) if obj.stage in self.TRACKER_STAGES else None
    )
    steps = []
    for index, name in enumerate(self.TRACKER_STAGES):
      if current_index is None:
        state = ""
      elif index < current_index:
        state = "done"
      elif name == obj.stage:
        state = "current"
      else:
        state = ""
      steps.append({"label": f"Step {index + 1}", "name": name, "state": state})
    return steps
