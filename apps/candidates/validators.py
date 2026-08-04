from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_desired_position(data):
  """
  Validates the DesiredPosition payload before saving.
  """
  errors = {}

  # Date Range Validation
  available_from = data.get("available_from")
  available_until = data.get("available_until")

  if available_from and available_until:
    if available_until < available_from:
      errors["available_until"] = ValidationError(
        _("The end date must be after the start date.")
      )

  # Freelance/Consulting Rate Validation
  engagement_types = data.get("engagement_types", [])

  # Check if freelance or consulting is in the list
  if "freelance" in engagement_types or "consulting" in engagement_types:
    if not data.get("min_daily_rate"):
      errors["min_daily_rate"] = ValidationError(
        _("A minimum daily rate is required for freelance or consulting positions.")
      )

  if errors:
    raise ValidationError(errors)
