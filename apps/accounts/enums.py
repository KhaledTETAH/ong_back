from django.db import models


class AuthProvider(models.TextChoices):
  EMAIL = "email", "Email"
  GOOGLE = "google", "Google"
  LINKEDIN = "linkedin", "LinkedIn"
  APPLE = "apple", "Apple"


class DocumentType(models.TextChoices):
  BYLAWS = "bylaws", "Bylaws"
  RECEIPT = "receipt", "Receipt"
  OFFICIAL_DECLARATION = "official_declaration", "Official declaration (RNA/RNE)"
  ACTIVITY_REPORT = "activity_report", "Activity report"
  ACCREDITATION = "accreditation", "Accreditation"


class Role(models.TextChoices):
  CANDIDATE = "candidate", "Candidate"
  NGO_MEMBER = "ngo_member", "NGO Member"
  VOLUNTEERING_REFERENT = "volunteering_referent", "Volunteering Referent"
  ADMIN = "admin", "Admin"
  MODERATOR = "moderator", "Moderator"


class Status(models.TextChoices):
  ACTIVE = "active", "Active"
  SUSPENDED = "suspended", "Suspended"
  BANNED = "banned", "Banned"
  PENDING = "pending", "Pending"
