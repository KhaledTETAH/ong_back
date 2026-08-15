from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import Cause, Country

from .models import Organization, OrganizationDocument

User = get_user_model()


class OrganizationListViewTest(APITestCase):
  def setUp(self):
    self.user = User.objects.create(
      email="testuser@gmail.com", password="testpassword123"
    )
    self.country = Country.objects.create(name="Algeria", code="DZA")
    self.cause = Cause.objects.create(name="Education")

    self.active_org = Organization.objects.create(
      name="Active NGO",
      owner=self.user,
      type="association",
      country=self.country,
      city="Oran",
      description="Test",
      is_active=True,
    )
    self.active_org.causes.add(self.cause)

    self.inactive_org = Organization.objects.create(
      name="Inactive NGO",
      owner=self.user,
      type="association",
      country=self.country,
      city="Algiers",
      description="Test",
      is_active=False,
    )

  def test_get_all_organizations(self):
    """
    Test that the list view returns only active organizations.
    """
    response = self.client.get("/api/v1/organizations/")

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data["success"])

    # Should only return 1 organization (the active one)
    self.assertEqual(len(response.data["data"]), 1)
    self.assertEqual(response.data["data"][0]["name"], "Active NGO")

  def test_inactive_organizations_excluded(self):
    """
    Test that inactive organizations are not in the list.
    """
    response = self.client.get("/api/v1/organizations/")
    org_names = [org["name"] for org in response.data["data"]]

    self.assertNotIn("Inactive NGO", org_names)


class OrganizationDetailViewTest(APITestCase):
  def setUp(self):
    self.user = User.objects.create(
      email="testuser@gmail.com", password="testpassword123"
    )
    self.country = Country.objects.create(name="France", code="FRA")
    self.cause = Cause.objects.create(name="Solidarity")

    self.active_org = Organization.objects.create(
      name="Active NGO Detail",
      owner=self.user,
      type="foundation",
      country=self.country,
      city="Paris",
      description="Test detail",
      is_active=True,
    )
    self.active_org.causes.add(self.cause)

    self.inactive_org = Organization.objects.create(
      name="Inactive NGO Detail",
      owner=self.user,
      type="ngo",
      country=self.country,
      city="Lyon",
      description="Test detail",
      is_active=False,
    )

  def test_get_active_organization(self):
    """
    Test fetching a valid, active organization by slug.
    """
    url = f"/api/v1/organizations/{self.active_org.slug}/"
    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data["success"])
    self.assertEqual(response.data["data"]["name"], "Active NGO Detail")
    cause_names = [c["name"] for c in response.data["data"]["causes"]]
    self.assertIn("Solidarity", cause_names)
    self.assertEqual(response.data["data"]["country"]["name_fr"], "France")
    self.assertIn("number_of_volunteers", response.data["data"])
    self.assertIn("open_offers_count", response.data["data"])
    self.assertIn("documents", response.data["data"])
    self.assertEqual(response.data["data"]["documents"], [])

  def test_get_organization_with_documents(self):
    """
    Test that transparency documents are included in the response.
    """
    OrganizationDocument.objects.create(
      organization=self.active_org,
      document_type="bylaws",
      file_url="https://example.com/bylaws.pdf",
      file_name="statuts.pdf",
      verified=True,
    )

    url = f"/api/v1/organizations/{self.active_org.slug}/"
    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    documents = response.data["data"]["documents"]
    self.assertEqual(len(documents), 1)
    self.assertEqual(documents[0]["document_type"], "bylaws")
    self.assertEqual(documents[0]["label"], "Bylaws")

  def test_get_nonexistent_organization(self):
    """
    Test that fetching a non-existent slug returns 404.
    """
    url = "/api/v1/organizations/nonexistent-org/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_inactive_organization(self):
    """
    Test that fetching an inactive organization returns 404.
    """
    url = f"/api/v1/organizations/{self.inactive_org.slug}/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
