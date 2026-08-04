import hashlib
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True


class Country(models.Model):
  code = models.CharField(max_length=2, primary_key=True)
  name_fr = models.CharField(max_length=120)
  is_covered = models.BooleanField(default=True)
  sort_order = models.PositiveIntegerField(default=100)

  class Meta:
    ordering = ["sort_order", "name_fr"]

  def __str__(self):
    return self.name_fr


class Cause(models.Model):
  name = models.CharField(max_length=120)
  slug = models.SlugField(unique=True)
  is_active = models.BooleanField(default=True)

  class Meta:
    ordering = ["name"]

  def __str__(self):
    return self.name


class Skill(models.Model):
  name = models.CharField(max_length=120)
  slug = models.SlugField(unique=True)
  is_active = models.BooleanField(default=True)

  class Meta:
    ordering = ["name"]

  def __str__(self):
    return self.name


class Language(models.Model):
  code = models.CharField(max_length=10, unique=True)
  name_fr = models.CharField(max_length=120)
  is_active = models.BooleanField(default=True)

  class Meta:
    ordering = ["name_fr"]

  def __str__(self):
    return self.name_fr


class Organization(TimeStampedModel):
  VERIFICATION_CHOICES = [
    ("pending", "Pending"),
    ("verified", "Verified"),
    ("certified_plus", "Certified plus"),
  ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="engagement_organizations",
  )
  name = models.CharField(max_length=180)
  slug = models.SlugField(unique=True, blank=True)
  type = models.CharField(max_length=40)
  country = models.ForeignKey(
    Country, on_delete=models.PROTECT, related_name="organizations"
  )
  city = models.CharField(max_length=120)
  registry_number = models.CharField(max_length=120, blank=True)
  size = models.CharField(max_length=40, blank=True)
  description = models.TextField()
  mission = models.TextField(blank=True)
  website = models.URLField(blank=True)
  verification_status = models.CharField(
    max_length=40, choices=VERIFICATION_CHOICES, default="pending"
  )
  is_active = models.BooleanField(default=True)
  causes = models.ManyToManyField(Cause, related_name="organizations", blank=True)

  class Meta:
    ordering = ["name"]

  def save(self, *args, **kwargs):
    if not self.slug:
      base = slugify(self.name) or "organization"
      slug = base
      counter = 1
      while Organization.objects.filter(slug=slug).exclude(pk=self.pk).exists():
        counter += 1
        slug = f"{base}-{counter}"
      self.slug = slug
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name


class Offer(TimeStampedModel):
  ENGAGEMENT_TYPES = [
    ("employment", "Employment"),
    ("volunteering", "Volunteering"),
    ("skills_sponsorship", "Skills sponsorship"),
    ("governance", "Governance"),
    ("consulting", "Consulting"),
    ("freelance", "Freelance"),
  ]
  REMOTE_MODES = [
    ("on_site", "On site"),
    ("hybrid", "Hybrid"),
    ("remote", "Remote"),
  ]
  STATUS_CHOICES = [
    ("draft", "Draft"),
    ("published", "Published"),
    ("closed", "Closed"),
  ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  organization = models.ForeignKey(
    Organization, on_delete=models.CASCADE, related_name="offers"
  )
  title = models.CharField(max_length=180)
  slug = models.SlugField(unique=True, blank=True)
  engagement_type = models.CharField(max_length=40, choices=ENGAGEMENT_TYPES)
  employment_contract = models.CharField(max_length=40, blank=True)
  country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="offers")
  city = models.CharField(max_length=120, blank=True)
  region = models.CharField(max_length=120, blank=True)
  remote_mode = models.CharField(max_length=40, choices=REMOTE_MODES, default="on_site")
  description = models.TextField()
  responsibilities = models.TextField(blank=True)
  desired_profile = models.TextField(blank=True)
  conditions = models.TextField(blank=True)
  duration_label = models.CharField(max_length=120, blank=True)
  duration_days = models.PositiveIntegerField(null=True, blank=True)
  experience_level = models.CharField(max_length=40, blank=True)
  status = models.CharField(max_length=40, choices=STATUS_CHOICES, default="published")
  published_at = models.DateTimeField(default=timezone.now)
  expires_at = models.DateTimeField(null=True, blank=True)
  featured = models.BooleanField(default=False)
  views_count = models.PositiveIntegerField(default=0)
  causes = models.ManyToManyField(Cause, related_name="offers", blank=True)
  languages = models.ManyToManyField(Language, related_name="offers", blank=True)
  skills = models.ManyToManyField(Skill, related_name="offers", blank=True)

  class Meta:
    ordering = ["-featured", "-published_at"]

  def save(self, *args, **kwargs):
    if not self.slug:
      base = slugify(self.title) or "offer"
      slug = base
      counter = 1
      while Offer.objects.filter(slug=slug).exclude(pk=self.pk).exists():
        counter += 1
        slug = f"{base}-{counter}"
      self.slug = slug
    super().save(*args, **kwargs)

  @property
  def is_published(self):
    return self.status == "published" and (
      self.expires_at is None or self.expires_at > timezone.now()
    )

  def __str__(self):
    return self.title


class Application(TimeStampedModel):
  offer = models.ForeignKey(
    Offer, on_delete=models.CASCADE, related_name="applications"
  )
  candidate = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
  )
  cover_letter = models.TextField(blank=True)
  status = models.CharField(max_length=40, default="new")
  applied_at = models.DateTimeField(default=timezone.now)

  class Meta:
    unique_together = ["offer", "candidate"]


class SavedOffer(TimeStampedModel):
  offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="saved_by")
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_offers"
  )

  class Meta:
    unique_together = ["offer", "user"]


class OfferEvent(TimeStampedModel):
  offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="events")
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
  )
  event_type = models.CharField(max_length=40)
  channel = models.CharField(max_length=40, blank=True)
  ip_hash = models.CharField(max_length=64, blank=True)
  user_agent_hash = models.CharField(max_length=64, blank=True)

  @staticmethod
  def digest(value):
    return hashlib.sha256((value or "").encode("utf-8")).hexdigest()


class SponsorSlot(TimeStampedModel):
  placement = models.CharField(max_length=80)
  sponsor_name = models.CharField(max_length=180)
  label = models.CharField(max_length=80, blank=True)
  copy = models.TextField(blank=True)
  target_url = models.URLField(blank=True)
  starts_at = models.DateTimeField(default=timezone.now)
  ends_at = models.DateTimeField(null=True, blank=True)
  is_active = models.BooleanField(default=True)

  @property
  def is_current(self):
    now = timezone.now()
    return (
      self.is_active
      and self.starts_at <= now
      and (self.ends_at is None or self.ends_at >= now)
    )


class SponsorshipMission(TimeStampedModel):
  VISIBILITY_CHOICES = [
    ("open", "Open"),
    ("verified_organizations", "Verified organizations"),
  ]
  STATUS_CHOICES = [
    ("pending_email_verification", "Pending email verification"),
    ("submitted", "Submitted"),
  ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  tracking_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
  contact_email = models.EmailField()
  company_name = models.CharField(max_length=180)
  company_legal_id = models.CharField(max_length=120, blank=True)
  country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
  region = models.CharField(max_length=120, blank=True)
  title = models.CharField(max_length=180)
  description = models.TextField(blank=True)
  objectives = models.TextField(blank=True)
  deliverables = models.TextField(blank=True)
  required_profiles = models.TextField(blank=True)
  man_days = models.PositiveIntegerField()
  visibility = models.CharField(max_length=40, choices=VISIBILITY_CHOICES)
  status = models.CharField(
    max_length=40, choices=STATUS_CHOICES, default="pending_email_verification"
  )
  verification_token_hash = models.CharField(max_length=64)
  verified_email_at = models.DateTimeField(null=True, blank=True)
  causes = models.ManyToManyField(
    Cause, related_name="sponsorship_missions", blank=True
  )

  def verify(self, token):
    if not self.token_matches(token):
      return False
    if self.verified_email_at is None:
      self.verified_email_at = timezone.now()
      self.status = "submitted"
      self.save(update_fields=["verified_email_at", "status", "updated_at"])
    return True

  def token_matches(self, token):
    return (
      self.verification_token_hash
      == hashlib.sha256((token or "").encode("utf-8")).hexdigest()
    )
