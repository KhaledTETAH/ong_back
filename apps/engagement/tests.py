from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.enums import Role, Status
from .models import Cause, Country, Language, Offer, Organization, Skill, SponsorSlot


class FirstSixPagesApiTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		User = get_user_model()

		self.candidate = User.objects.create_user(
			email="candidate@example.test",
			password="Password123!",
			role=Role.CANDIDATE,
			status=Status.ACTIVE,
			email_verified=True,
		)
		self.owner = User.objects.create_user(
			email="owner@example.test",
			password="Password123!",
			role=Role.NGO_MEMBER,
			status=Status.ACTIVE,
			email_verified=True,
		)
		self.country = Country.objects.create(code="DZ", name_fr="Algerie", is_covered=True)
		self.cause = Cause.objects.create(name="Education", slug="education")
		self.language = Language.objects.create(code="fr", name_fr="Francais")
		self.skill = Skill.objects.create(name="Gestion de projet", slug="gestion-de-projet")
		self.organization = Organization.objects.create(
			owner=self.owner,
			name="Association Lumiere d'Oran",
			slug="association-lumiere-doran",
			type="association",
			country=self.country,
			city="Oran",
			registry_number="DZ-001",
			description="Association d'education.",
			verification_status="verified",
			is_active=True,
		)
		self.organization.causes.add(self.cause)
		self.offer = Offer.objects.create(
			organization=self.organization,
			title="Coordinateur education",
			slug="coordinateur-education-1",
			engagement_type="employment",
			country=self.country,
			city="Oran",
			remote_mode="on_site",
			description="Coordination du programme education.",
			duration_label="6 mois",
			duration_days=180,
			experience_level="confirmed",
			featured=True,
			status="published",
		)
		self.offer.causes.add(self.cause)
		self.offer.languages.add(self.language)
		self.offer.skills.add(self.skill)
		SponsorSlot.objects.create(placement="homepage", sponsor_name="Partenaire ethique", is_active=True)

	def authenticate_candidate(self):
		response = self.client.post(reverse("token_obtain_pair"), {"email": "candidate@example.test", "password": "Password123!"}, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['data']['access']}")

	def test_home_offers_and_organizations_are_public(self):
		self.assertEqual(self.client.get(reverse("home")).status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.get(reverse("offers"), {"q": "education", "country": "DZ"}).status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.get(reverse("offer_detail", args=[self.offer.slug])).status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.get(reverse("offer_similar", args=[self.offer.slug])).status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.get(reverse("organizations"), {"country": "DZ", "cause": "education"}).status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.get(reverse("organization_detail", args=[self.organization.slug])).status_code, status.HTTP_200_OK)

	def test_sponsorship_submission_tracking_and_verification(self):
		response = self.client.post(
			reverse("sponsorship_create"),
			{
				"contact_email": "mecenat@example.test",
				"company_name": "Entreprise Solidaire",
				"country_code": "DZ",
				"title": "Audit solidaire",
				"description": "Mission de test.",
				"man_days": 5,
				"visibility": "verified_organizations",
				"cause_ids": [self.cause.id],
				"consent": True,
				"website": "",
			},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		token = response.data["data"]["debug_verification_token"]
		tracking_uuid = response.data["data"]["tracking_uuid"]
		self.assertEqual(self.client.get(reverse("sponsorship_detail", args=[tracking_uuid]), {"token": token}).status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.post(reverse("sponsorship_verify", args=[tracking_uuid]), {"token": token}, format="json").status_code, status.HTTP_200_OK)

	def test_candidate_can_save_apply_and_share_offer(self):
		self.authenticate_candidate()
		self.assertEqual(self.client.put(reverse("offer_saved", args=[self.offer.slug])).status_code, status.HTTP_200_OK)
		self.assertEqual(
			self.client.post(reverse("offer_apply", args=[self.offer.slug]), {"cover_letter": "Je souhaite contribuer."}, format="json").status_code,
			status.HTTP_201_CREATED,
		)
		self.assertEqual(self.client.post(reverse("offer_share", args=[self.offer.slug]), {"channel": "copy_link"}, format="json").status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.delete(reverse("offer_saved", args=[self.offer.slug])).status_code, status.HTTP_200_OK)

	def test_registration_endpoints(self):
		candidate = self.client.post(
			reverse("register_candidate"),
			{"email": "new-candidate@example.test", "password": "Password123!", "phone": "+213555000000"},
			format="json",
		)
		self.assertEqual(candidate.status_code, status.HTTP_201_CREATED)

		organization = self.client.post(
			reverse("register_organization"),
			{
				"owner_email": "new-owner@example.test",
				"password": "Password123!",
				"organization_name": "ONG Test",
				"organization_type": "ngo",
				"country_code": "DZ",
				"city": "Oran",
				"registry_number": "REG-001",
				"description": "Organisation de test.",
			},
			format="json",
		)
		self.assertEqual(organization.status_code, status.HTTP_201_CREATED)
