from django.db import models


# organization enums
class OrganizationType(models.TextChoices):
  NGO = "ngo", "NGO"
  ASSOCIATION = "association", "Association"
  FOUNDATION = "foundation", "Foundation"
  WAQF = "waqf", "Waqf"
  HUMANITARIAN = "humanitarian", "Humanitarian organization"
  CHARITABLE = "charitable", "Charitable organization"


class VerificationStatus(models.TextChoices):
  IN_PROGRESS = "in_progress", "In progress"
  VERIFIED = "verified", "Verified"
  CERTIFIED_PLUS = "certified_plus", "Certified+"


class DocumentType(models.TextChoices):
  BYLAWS = "bylaws", "Bylaws"
  RECEIPT = "receipt", "Receipt"
  OFFICIAL_DECLARATION = (
    "official_declaration",
    "Official declaration (RNA/RNE/national registry)",
  )
  ACTIVITY_REPORT = "activity_report", "Activity report"


class MemberRole(models.TextChoices):
  ADMIN = "admin", "Admin"
  RECRUITER = "recruiter", "Recruiter"
  READER = "reader", "Reader"


# offer enums
class OfferStatus(models.TextChoices):
  DRAFT = "draft", "Draft"
  PUBLISHED = "published", "Published"
  CLOSED = "closed", "Closed"


class ContractType(models.TextChoices):
  PERMANENT = "permanent", "Permanent (CDI)"
  FIXED_TERM = "fixed_term", "Fixed-term (CDD)"
  APPRENTICESHIP = "apprenticeship", "Apprenticeship"
  CIVIC_SERVICE = "civic_service", "Civic service"
  VSI = "vsi", "VSI"
  VIE = "vie", "VIE"


class ExperienceLevel(models.TextChoices):
  JUNIOR = "junior", "Junior"
  CONFIRMED = "confirmed", "Confirmed"
  SENIOR = "senior", "Senior"
  EXPERT = "expert", "Expert"
  MANDATE = "mandate", "Mandate"


class OfferVisibility(models.TextChoices):
  OPEN = "open", "Open"
  TARGETED = "targeted", "Targeted (Verified NGOs)"
  PRIVATE = "private", "Private (Direct invitation)"
