from django.db import models


class Availability(models.TextChoices):
  FULL_TIME = "full_time", "Full-time"
  PART_TIME = "part_time", "Part-time"
  OCCASIONAL = "occasional", "Occasional"
  EVENINGS = "evenings", "Evenings"
  WEEKENDS = "weekends", "Weekends"


class Mobility(models.TextChoices):
  LOCAL = "local", "Local"
  REGIONAL = "regional", "Regional"
  NATIONAL = "national", "National"
  INTERNATIONAL = "international", "International"
  FIELD = "field", "Field"


class PositionLevel(models.TextChoices):
  JUNIOR = "junior", "Junior"
  CONFIRMED = "confirmed", "Confirmed"
  SENIOR = "senior", "Senior"
  EXPERT = "expert", "Expert"
  MANDATE = "mandate", "Mandate"
