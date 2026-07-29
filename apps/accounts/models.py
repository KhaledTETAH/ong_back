import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .enums import AuthProvider, Role, Status

class UserManager(BaseUserManager):
	"""
	Custom user manager where email is the unique identifier.
	"""

	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The Email field must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('role', Role.ADMIN)
		extra_fields.setdefault('status', Status.ACTIVE)
		return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	email = models.EmailField(unique=True, verbose_name="email address")

	auth_provider = models.CharField(max_length=20, choices=AuthProvider.choices, default=AuthProvider.EMAIL)
	external_auth_id = models.CharField(max_length=255, null=True, blank=True)
	email_verified = models.BooleanField(default=False)
	
	phone = models.CharField(max_length=20, null=True, blank=True)
	phone_verified = models.BooleanField(default=False)
	
	role = models.CharField(max_length=30, choices=Role.choices, default=Role.CANDIDATE)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	
	notification_prefs = models.JSONField(default=dict, blank=True)
	

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email