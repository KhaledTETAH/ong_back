import uuid
from django.db import models
from django.utils.text import slugify

class Cause(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(unique=True, blank=True)
	description = models.TextField(blank=True)
	# Optional: icon or color for the UI tags
	icon_url = models.URLField(blank=True) 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "causes"
		ordering = ["name"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

class Country(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=100, unique=True)
	code = models.CharField(max_length=3, unique=True) # e.g., "DZA", "FRA"
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name




class Language(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=100, unique=True) # e.g., "French", "English"
	code = models.CharField(max_length=10, unique=True)  # e.g., "FR", "EN"
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Skill(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=150, unique=True) # e.g., "Project Management", "Python"
	slug = models.SlugField(unique=True, blank=True)
	category = models.CharField(max_length=50, blank=True) # Optional: e.g., "Hard Skill", "Soft Skill"
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "skills"
		ordering = ["name"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)