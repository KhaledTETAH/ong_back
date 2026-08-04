import uuid
from django.conf import settings
from django.db import models
from .enums import Availability, Mobility, PositionLevel
from apps.core.models import *
from apps.core.enums import *


class CandidateProfile(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidate_profile"
  )

  # basic info
  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  bio = models.TextField(blank=True)
  photo_url = models.URLField(blank=True)
  cv_url = models.URLField(blank=True)

  # profile metrics
  profile_completion = models.PositiveSmallIntegerField(default=0)  # 0-100%
  is_expert_profile = models.BooleanField(default=False)  # "Profil expert" badge

  # availability toggle
  actively_looking = models.BooleanField(default=False)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Profile of {self.user.email}"


class DesiredPosition(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  candidate = models.OneToOneField(
    CandidateProfile, on_delete=models.CASCADE, related_name="desired_position"
  )

  # engagement types sought
  engagement_types = models.JSONField(default=list, blank=True)
  # multi select validated against EngagementType.choices

  # causes (preferred and excluded)
  preferred_causes = models.ManyToManyField(
    Cause, related_name="desired_by_candidates", blank=True
  )
  excluded_causes = models.ManyToManyField(
    Cause, related_name="excluded_by_candidates", blank=True
  )

  # modalities
  modalities = models.JSONField(default=list, blank=True)
  # multi select validated against RemoteMode.choices

  # availability details
  availability = models.CharField(
    max_length=20, choices=Availability.choices, blank=True
  )

  # mobility
  mobility = models.CharField(max_length=20, choices=Mobility.choices, blank=True)

  # position level
  position_level = models.CharField(
    max_length=20, choices=PositionLevel.choices, blank=True
  )

  # geographic preferences
  preferred_geographies = models.ManyToManyField(
    Country, related_name="desired_by_candidates", blank=True
  )

  # skills
  skills_to_leverage = models.ManyToManyField(
    Skill, related_name="leveraged_by_candidates", blank=True
  )
  skills_to_develop = models.ManyToManyField(
    Skill, related_name="developed_by_candidates", blank=True
  )

  # freelance/Consulting specific
  min_daily_rate = models.DecimalField(
    max_digits=10, decimal_places=2, null=True, blank=True
  )

  # availability dates
  available_from = models.DateField(null=True, blank=True)
  available_until = models.DateField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Desired position for {self.candidate.user.email}"
