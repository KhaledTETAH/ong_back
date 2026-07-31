import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from .enums import *
from apps.core.models import Country, Cause, Language, Skill

class Organization(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organizations")
	name = models.CharField(max_length=180)
	slug = models.SlugField(unique=True, blank=True)
	type = models.CharField(max_length=40, choices=OrganizationType.choices, default=OrganizationType.ASSOCIATION)

	country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="organizations")
	city = models.CharField(max_length=120)
	registry_number = models.CharField(max_length=120, blank=True)
	size = models.CharField(max_length=40, blank=True) 
	description = models.TextField()
	mission = models.TextField(blank=True)
	website = models.URLField(blank=True)
	verification_status = models.CharField(
			max_length=40, 
			choices=VerificationStatus.choices, 
			default=VerificationStatus.IN_PROGRESS
	)
	causes = models.ManyToManyField(Cause, related_name="organizations", blank=True)
	is_active = models.BooleanField(default=True)
	founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
	logo_url = models.URLField(blank=True)
	banner_url = models.URLField(blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		# auto-generate slug from name if not provided
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


class OrganizationDocument(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="documents")
	document_type = models.CharField(max_length=40, choices=DocumentType.choices)
	file_url = models.URLField()
	file_name = models.CharField(max_length=180, blank=True)
	verified = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["document_type"]

	def __str__(self):
		return f"{self.organization.name} - {self.get_document_type_display()}"


class OrganizationMember(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization_memberships")
	
	role = models.CharField(max_length=40, choices=MemberRole.choices, default=MemberRole.READER)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ["organization", "user"]

	def __str__(self):
		return f"{self.user} - {self.organization.name} ({self.role})"


class Follow(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follows")
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="followers")

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ["user", "organization"]

	def __str__(self):
		return f"{self.user} follows {self.organization.name}"


class Offer(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="offers")
	
	title = models.CharField(max_length=180)
	slug = models.SlugField(unique=True, blank=True)
	
	engagement_type = models.CharField(max_length=40, choices=EngagementType.choices)
	employment_contract = models.CharField(max_length=40, choices=ContractType.choices, blank=True)
	experience_level = models.CharField(max_length=40, choices=ExperienceLevel.choices, blank=True)
	
	country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="offers")
	city = models.CharField(max_length=120, blank=True)
	region = models.CharField(max_length=120, blank=True)
	remote_mode = models.CharField(max_length=40, choices=RemoteMode.choices, default=RemoteMode.ON_SITE)
	
	description = models.TextField()
	responsibilities = models.TextField(blank=True)
	desired_profile = models.TextField(blank=True)
	conditions = models.TextField(blank=True)
	
	budget = models.CharField(max_length=120, blank=True) 
	
	duration_label = models.CharField(max_length=120, blank=True)
	duration_days = models.PositiveIntegerField(null=True, blank=True)
	
	status = models.CharField(max_length=40, choices=OfferStatus.choices, default=OfferStatus.DRAFT)
	
	visibility = models.CharField(max_length=20, choices=OfferVisibility.choices, default=OfferVisibility.OPEN)
	
	published_at = models.DateTimeField(null=True, blank=True)
	expires_at = models.DateTimeField(null=True, blank=True)
	
	featured = models.BooleanField(default=False)
	views_count = models.PositiveIntegerField(default=0)
	
	causes = models.ManyToManyField(Cause, related_name="offers", blank=True)
	languages = models.ManyToManyField(Language, related_name="offers", blank=True)
	skills = models.ManyToManyField(Skill, related_name="offers", blank=True)


	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

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
		return self.status == OfferStatus.PUBLISHED and (self.expires_at is None or self.expires_at > timezone.now())

	def __str__(self):
		return self.title