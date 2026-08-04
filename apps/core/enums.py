from django.db import models


class EngagementType(models.TextChoices):
  EMPLOYMENT = "employment", "Employment"
  VOLUNTEERING = "volunteering", "Volunteering"
  SKILLS_BASED_VOLUNTEERING = "skills_based_volunteering", "Skills-based volunteering"
  GOVERNANCE = "governance", "Governance"
  CONSULTING = "consulting", "Consulting"
  FREELANCE = "freelance", "Freelance"


class RemoteMode(models.TextChoices):
  ON_SITE = "on_site", "On site"
  HYBRID = "hybrid", "Hybrid"
  REMOTE = "remote", "Remote"
