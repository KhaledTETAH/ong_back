from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.enums import Role, Status
from apps.engagement.models import Cause, Country, Language, Offer, Organization, Skill, SponsorSlot


class Command(BaseCommand):
	help = "Seed demo data for the first six engagement-platform pages."

	def handle(self, *args, **options):
		countries = {
			"DZ": Country.objects.update_or_create(code="DZ", defaults={"name_fr": "Algerie", "is_covered": True, "sort_order": 1})[0],
			"FR": Country.objects.update_or_create(code="FR", defaults={"name_fr": "France", "is_covered": True, "sort_order": 2})[0],
			"MA": Country.objects.update_or_create(code="MA", defaults={"name_fr": "Maroc", "is_covered": True, "sort_order": 3})[0],
		}
		causes = {
			"education": Cause.objects.update_or_create(slug="education", defaults={"name": "Education"})[0],
			"inclusion-numerique": Cause.objects.update_or_create(slug="inclusion-numerique", defaults={"name": "Inclusion numerique"})[0],
			"jeunesse": Cause.objects.update_or_create(slug="jeunesse", defaults={"name": "Jeunesse"})[0],
		}
		languages = {
			"fr": Language.objects.update_or_create(code="fr", defaults={"name_fr": "Francais"})[0],
			"ar": Language.objects.update_or_create(code="ar", defaults={"name_fr": "Arabe"})[0],
		}
		skills = {
			"gestion-de-projet": Skill.objects.update_or_create(slug="gestion-de-projet", defaults={"name": "Gestion de projet"})[0],
			"developpement-web": Skill.objects.update_or_create(slug="developpement-web", defaults={"name": "Developpement web"})[0],
		}

		User = get_user_model()
		candidate, _ = User.objects.update_or_create(
			email="candidat@example.test",
			defaults={"role": Role.CANDIDATE, "status": Status.ACTIVE, "email_verified": True},
		)
		candidate.set_password("Password123!")
		candidate.save()

		owner, _ = User.objects.update_or_create(
			email="organisation@example.test",
			defaults={"role": Role.NGO_MEMBER, "status": Status.ACTIVE, "email_verified": True},
		)
		owner.set_password("Password123!")
		owner.save()

		org, _ = Organization.objects.update_or_create(
			slug="association-lumiere-doran",
			defaults={
				"owner": owner,
				"name": "Association Lumiere d'Oran",
				"type": "association",
				"country": countries["DZ"],
				"city": "Oran",
				"registry_number": "DZ-ORN-2014-00872",
				"size": "medium",
				"description": "Association active dans l'education et l'inclusion numerique.",
				"mission": "Reduire les inegalites educatives.",
				"verification_status": "verified",
				"is_active": True,
			},
		)
		org.causes.set([causes["education"], causes["jeunesse"], causes["inclusion-numerique"]])

		offer, _ = Offer.objects.update_or_create(
			slug="coordinateur-education-1",
			defaults={
				"organization": org,
				"title": "Coordinateur education",
				"engagement_type": "employment",
				"employment_contract": "cdd",
				"country": countries["DZ"],
				"city": "Oran",
				"remote_mode": "on_site",
				"description": "Coordination d'un programme d'accompagnement scolaire.",
				"responsibilities": "Planifier les activites et coordonner les benevoles.",
				"desired_profile": "Experience en coordination de projet.",
				"conditions": "CDD de 6 mois.",
				"duration_label": "6 mois",
				"duration_days": 180,
				"experience_level": "confirmed",
				"status": "published",
				"published_at": timezone.now(),
				"featured": True,
			},
		)
		offer.causes.set([causes["education"], causes["jeunesse"]])
		offer.languages.set([languages["fr"], languages["ar"]])
		offer.skills.set([skills["gestion-de-projet"]])

		web_offer, _ = Offer.objects.update_or_create(
			slug="developpeur-web-benevole-2",
			defaults={
				"organization": org,
				"title": "Developpeur web benevole",
				"engagement_type": "volunteering",
				"country": countries["DZ"],
				"city": "Oran",
				"remote_mode": "remote",
				"description": "Ameliorer un outil interne de suivi.",
				"duration_label": "8 semaines",
				"duration_days": 56,
				"experience_level": "confirmed",
				"status": "published",
				"published_at": timezone.now(),
			},
		)
		web_offer.causes.set([causes["education"], causes["inclusion-numerique"]])
		web_offer.languages.set([languages["fr"]])
		web_offer.skills.set([skills["developpement-web"]])

		SponsorSlot.objects.update_or_create(
			placement="homepage",
			defaults={
				"sponsor_name": "Partenaire ethique",
				"label": "Partenariat",
				"copy": "Emplacement reserve a un partenaire aligne avec les valeurs de la plateforme.",
				"is_active": True,
			},
		)
		self.stdout.write(self.style.SUCCESS("Demo data seeded."))
