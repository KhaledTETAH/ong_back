from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.enums import Role, Status
from apps.core.models import Country
from apps.organizations.enums import OrganizationType, VerificationStatus
from apps.organizations.models import Offer, Organization

from .models import Application, CandidateProfile

User = get_user_model()


class DesiredPositionViewTests(TestCase):
  """
  Tests for the desired position GET endpoint (page 9 prefill).
  """

  def setUp(self):
    """
    Set up a client and an authenticated candidate.
    """
    self.client = APIClient()

    self.user = User.objects.create_user(
      email="fica@example.com",
      password="securepassword123",
      role=Role.CANDIDATE,
      status=Status.ACTIVE,
      email_verified=True,
    )
    self.client.force_authenticate(user=self.user)
    self.url = reverse("candidates:desired_position")

  def test_get_creates_and_returns_default(self):
    """
    Test: GET creates an empty DesiredPosition and returns it.
    """
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data["success"])
    self.assertEqual(response.data["data"]["position_title"], "")
    self.assertEqual(response.data["data"]["email_alerts"], False)

  def test_put_updates_position_title(self):
    """
    Test: PUT persists the desired position fields.
    """
    self.client.put(
      self.url, {"position_title": "Chef de projet éducation"}, format="json"
    )
    response = self.client.get(self.url)
    self.assertEqual(
      response.data["data"]["position_title"], "Chef de projet éducation"
    )


class MyCandidacyViewTests(TestCase):
  """
  Tests for the authenticated candidate dashboard endpoint.
  """

  def setUp(self):
    """
    Set up a client, an authenticated candidate and a published offer.
    """
    self.client = APIClient()

    self.user = User.objects.create_user(
      email="candidate@example.com",
      password="securepassword123",
      role=Role.CANDIDATE,
      status=Status.ACTIVE,
      email_verified=True,
    )
    self.client.force_authenticate(user=self.user)

    country = Country.objects.create(name="France", code="FRA")
    org = Organization.objects.create(
      owner=self.user,
      name="Test Org",
      type=OrganizationType.ASSOCIATION,
      country=country,
      city="Paris",
      verification_status=VerificationStatus.VERIFIED,
    )
    self.offer = Offer.objects.create(
      organization=org,
      title="Coordinateur",
      engagement_type="volunteering",
      country=country,
      city="Paris",
      description="Mission de coordination.",
    )

    self.url = reverse("candidates:my_applications")

  def test_requires_authentication(self):
    """
    Test: unauthenticated request is rejected.
    """
    client = APIClient()
    response = client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_returns_empty_dashboard(self):
    """
    Test: a candidate with no applications gets a valid empty dashboard.
    """
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data["success"])
    self.assertEqual(response.data["data"]["applications_count"], 0)
    self.assertEqual(response.data["data"]["applications"], [])

  def test_returns_application_with_tracker(self):
    """
    Test: applications are listed with offer/org info and a tracker.
    """
    profile = CandidateProfile.objects.create(user=self.user, first_name="Amine")
    Application.objects.create(candidate=profile, offer=self.offer, stage="interview")

    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = response.data["data"]
    self.assertEqual(data["applications_count"], 1)
    self.assertEqual(data["first_name"], "Amine")

    application = data["applications"][0]
    self.assertEqual(application["offer"], "Coordinateur")
    self.assertEqual(application["org"], "Test Org")
    self.assertEqual(application["stage"], "interview")

    tracker_stages = [step["name"] for step in application["tracker"]]
    self.assertEqual(
      tracker_stages,
      [
        "submitted",
        "prequalified",
        "interview",
        "decision",
        "offer",
      ],
    )
    states = [step["state"] for step in application["tracker"]]
    self.assertEqual(states, ["done", "done", "current", "", ""])
