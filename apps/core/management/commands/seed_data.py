"""
Management command: seed the database with realistic demo/test data.

Usage:
        python manage.py seed_data              # seed without wiping existing data
        python manage.py seed_data --flush       # wipe the whole DB first, then seed

What gets created (in order):
        1. Core taxonomies   -> Country, Cause, Language, Skill
        2. Users             -> admin, NGO owner, NGO recruiter, candidate, referent
        3. Organizations     -> 3 sample NGOs/associations/foundations
        4. Org documents     -> sample transparency documents for org1
        5. Org members       -> owner + recruiter attached to org1
        6. Follows           -> candidate follows org1 and org2
        7. Offers            -> sample volunteering/freelance/consulting offers for org1
        8. Candidate space   -> candidate profile, desired position fiche, applications

All creation helpers use get_or_create, so re-running the command without
--flush is idempotent (it won't create duplicates).
"""

import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.enums import AuthProvider, Role, Status
from apps.candidates.enums import (
  ApplicationStage,
  Availability,
  Mobility,
  PositionLevel,
)
from apps.candidates.models import Application, CandidateProfile, DesiredPosition
from apps.core.enums import EngagementType, RemoteMode
from apps.core.models import Cause, Country, Language, Skill
from apps.organizations.enums import (
  DocumentType,
  MemberRole,
  OfferStatus,
  OrganizationType,
  VerificationStatus,
)
from apps.organizations.models import (
  Follow,
  Offer,
  Organization,
  OrganizationDocument,
  OrganizationMember,
)

User = get_user_model()


class Command(BaseCommand):
  help = (
    "Seeds the database with realistic test data. Use --flush to wipe the DB first."
  )

  def add_arguments(self, parser):
    """Register the --flush CLI flag."""
    parser.add_argument(
      "--flush",
      action="store_true",
      help="Wipe the entire database before seeding.",
    )

  def handle(self, *args, **options):
    """
    Entry point called by `manage.py seed_data`.

    Orchestrates the seeding process step by step: taxonomies, users,
    organizations, documents, memberships, follows, and offers.
    """
    if options["flush"]:
      self.stdout.write(self.style.WARNING("Flushing database..."))
      call_command("flush", "--no-input")
      self.stdout.write(self.style.SUCCESS("Database flushed successfully."))

    self.stdout.write("Starting data seeding...")

    # 1. Core Taxonomies
    countries = self.seed_countries()
    causes = self.seed_causes()
    languages = self.seed_languages()
    skills = self.seed_skills()

    # 2. Users
    ngo_owner = self.create_user(
      "directeur@lumiere-oran.org", "password123", Role.NGO_MEMBER, Status.ACTIVE
    )
    ngo_recruiter = self.create_user(
      "recruteur@lumiere-oran.org", "password123", Role.NGO_MEMBER, Status.ACTIVE
    )
    candidate = self.create_user(
      "candidate@email.com", "password123", Role.CANDIDATE, Status.ACTIVE
    )

    # 3. Organizations
    org1 = self.create_organization(
      "Association Lumière d'Oran",
      ngo_owner,
      countries["DZA"],
      "Oran",
      OrganizationType.ASSOCIATION,
      VerificationStatus.VERIFIED,
      "12345",
      "2011",
      causes,
    )
    org2 = self.create_organization(
      "Fondation Espoir Maghreb",
      ngo_owner,
      countries["MAR"],
      "Casablanca",
      OrganizationType.FOUNDATION,
      VerificationStatus.CERTIFIED_PLUS,
      "F-9876",
      "2005",
      causes,
    )

    # 4. Organization Documents (For Transparency block)
    self.create_documents(org1, causes)

    # 5. Organization Members
    OrganizationMember.objects.create(
      organization=org1, user=ngo_owner, role=MemberRole.ADMIN
    )
    OrganizationMember.objects.create(
      organization=org1, user=ngo_recruiter, role=MemberRole.RECRUITER
    )

    # 6. Follows
    Follow.objects.create(user=candidate, organization=org1)
    Follow.objects.create(user=candidate, organization=org2)

    # 7. Offers
    offers = self.create_offers(org1, countries, causes, languages, skills)

    # 8. Candidate space (pages 8 & 9)
    self.seed_candidate(candidate, offers, countries, causes, skills)

    self.stdout.write(
      self.style.SUCCESS("Successfully seeded database with realistic data!")
    )
    self.stdout.write(
      self.style.SUCCESS("Admin login: admin@plateforme.org / admin123")
    )
    self.stdout.write(
      self.style.SUCCESS("NGO login: directeur@lumiere-oran.org / password123")
    )
    self.stdout.write(
      self.style.SUCCESS("Candidate login: candidate@email.com / password123")
    )

  # --- Helper Methods ---

  def create_user(self, email, password, role, status):
    """
    Get or create a user with the given email.

    If the user is newly created, set and hash the password.
    Existing users are returned unchanged (password is not reset).
    """
    user, created = User.objects.get_or_create(
      email=email,
      defaults={
        "role": role,
        "status": status,
        "email_verified": True,
        "auth_provider": AuthProvider.EMAIL,
      },
    )
    if created:
      user.set_password(password)
      user.save()
    return user

  def seed_countries(self):
    """Create the base set of countries and return a dict keyed by ISO code."""
    data = [
      ("France", "FRA"),
      ("Algérie", "DZA"),
      ("Maroc", "MAR"),
      ("Tunisie", "TUN"),
      ("Belgique", "BEL"),
      ("Suisse", "CHE"),
    ]
    countries = {}
    for name, code in data:
      obj, _ = Country.objects.get_or_create(code=code, defaults={"name": name})
      countries[code] = obj
    return countries

  def seed_causes(self):
    """Create the base set of causes and return a dict keyed by name."""
    data = [
      "Éducation",
      "Solidarité",
      "Jeunesse",
      "Environnement",
      "Santé",
      "Droits de l'homme",
    ]
    causes = {}
    for name in data:
      obj, _ = Cause.objects.get_or_create(name=name)
      causes[name] = obj
    return causes

  def seed_languages(self):
    """Create the base set of languages and return a dict keyed by name."""
    data = [("Français", "FR"), ("Anglais", "EN"), ("Arabe", "AR"), ("Espagnol", "ES")]
    languages = {}
    for name, code in data:
      obj, _ = Language.objects.get_or_create(code=code, defaults={"name": name})
      languages[name] = obj
    return languages

  def seed_skills(self):
    """Create the base set of skills and return a dict keyed by name."""
    data = [
      "Gestion de projet",
      "Communication",
      "Développement web",
      "Collecte de fonds",
      "Juridique",
      "Pédagogie",
    ]
    skills = {}
    for name in data:
      obj, _ = Skill.objects.get_or_create(name=name)
      skills[name] = obj
    return skills

  def create_organization(
    self, name, owner, country, city, org_type, verification, registry, founded, causes
  ):
    """
    Get or create an organization with generated description/mission text,
    a placeholder logo/banner, and a default set of causes (Éducation,
    Solidarité, Jeunesse) attached on first creation.
    """
    clean_name = name.lower().replace(" ", "").replace("'", "")
    website = f"https://www.{clean_name}.org"
    org, created = Organization.objects.get_or_create(
      name=name,
      defaults={
        "owner": owner,
        "country": country,
        "city": city,
        "type": org_type,
        "verification_status": verification,
        "registry_number": registry,
        "founded_year": int(founded),
        "description": (
          f"L'organisation {name} œuvre depuis {founded} pour le "
          "développement local et l'impact social. Elle accompagne les communautés "
          "à travers des programmes structurants et un réseau de bénévoles engagés."
        ),
        "mission": (
          "Promouvoir l'accès aux droits fondamentaux et renforcer les "
          f"capacités locales dans la région de {city}."
        ),
        "website": website,
        "is_active": True,
        "logo_url": "https://ui-avatars.com/api/?name="
        + name.replace(" ", "+")
        + "&background=0D9488&color=fff&size=128",
        "banner_url": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?auto=format&fit=crop&w=1200&q=80",
      },
    )
    if created:
      # Add causes
      org.causes.set([causes["Éducation"], causes["Solidarité"], causes["Jeunesse"]])
    return org

  def create_documents(self, org, causes):
    """
    Attach a fixed set of sample transparency documents (bylaws, official
    declaration, activity report) to the given organization.

    Note: the `causes` parameter is currently unused but kept for
    signature compatibility with the calling code.
    """
    docs = [
      (DocumentType.BYLAWS, "Statuts_Lumiere_Oran.pdf", True),
      (DocumentType.OFFICIAL_DECLARATION, "Declaration_RNA_12345.pdf", True),
      (DocumentType.ACTIVITY_REPORT, "Rapport_Activite_2024.pdf", True),
    ]
    for doc_type, filename, verified in docs:
      OrganizationDocument.objects.get_or_create(
        organization=org,
        document_type=doc_type,
        defaults={
          "file_url": f"https://example.com/docs/{filename}",
          "file_name": filename,
          "verified": verified,
        },
      )

  def create_offers(self, org, countries, causes, languages, skills):
    """
    Create a fixed set of sample offers (volunteering, freelance,
    consulting) for the given organization.

    Each offer's country is inferred from its city (Oran -> DZA,
    Casablanca -> MAR, otherwise -> FRA). Published offers get a random
    `published_at` timestamp within the last 30 days; draft offers get
    none. On first creation, each offer is tagged with a default set of
    causes, languages, and skills. Returns the created offers list.
    """
    offers_data = [
      {
        "title": "Coordinateur éducation",
        "type": EngagementType.VOLUNTEERING,
        "city": "Oran",
        "remote": RemoteMode.ON_SITE,
        "duration": "6 mois",
        "status": OfferStatus.PUBLISHED,
        "desc": (
          "Coordonner les programmes de soutien scolaire dans",
          "les quartiers défavorisés de l'ouest algérien.",
        ),
      },
      {
        "title": "Animateur jeunesse — été",
        "type": EngagementType.VOLUNTEERING,
        "city": "Oran",
        "remote": RemoteMode.ON_SITE,
        "duration": "2 mois",
        "status": OfferStatus.PUBLISHED,
        "desc": (
          "Animer les programmes d'été pour les enfants de 8 ",
          "à 14 ans (sports, culture, éducation).",
        ),
      },
      {
        "title": "Bibliothécaire bénévole",
        "type": EngagementType.VOLUNTEERING,
        "city": "Oran",
        "remote": RemoteMode.ON_SITE,
        "duration": "Récurrent",
        "status": OfferStatus.PUBLISHED,
        "desc": (
          "Gestion et animation de la bibliothèque de quartier, ",
          "aide aux devoirs et ateliers de lecture.",
        ),
      },
      {
        "title": "Chargé de communication digital",
        "type": EngagementType.FREELANCE,
        "city": "Casablanca",
        "remote": RemoteMode.HYBRID,
        "duration": "3 mois",
        "status": OfferStatus.PUBLISHED,
        "desc": (
          "Piloter la stratégie réseaux sociaux et créer du contenu ",
          "engageant pour nos campagnes de sensibilisation.",
        ),
      },
      {
        "title": "Consultant collecte de fonds",
        "type": EngagementType.CONSULTING,
        "city": "Paris",
        "remote": RemoteMode.REMOTE,
        "duration": "1 mois",
        "status": OfferStatus.DRAFT,
        "desc": (
          "Audit et mise en place d'une stratégie ",
          "de fundraising pour notre campagne annuelle.",
        ),
      },
    ]

    offers = []
    for data in offers_data:
      offer, created = Offer.objects.get_or_create(
        title=data["title"],
        organization=org,
        defaults={
          "engagement_type": data["type"],
          "country": countries["DZA"]
          if data["city"] == "Oran"
          else countries["MAR"]
          if data["city"] == "Casablanca"
          else countries["FRA"],
          "city": data["city"],
          "remote_mode": data["remote"],
          "duration_label": data["duration"],
          "status": data["status"],
          "description": data["desc"],
          "desired_profile": (
            "Profil engagé, autonome, avec une première ",
            "expérience dans le secteur associatif.",
          ),
          "conditions": "Frais de transport remboursés. Repas fournis sur place.",
          "budget": "Gratuit / Bénévolat"
          if data["type"] == EngagementType.VOLUNTEERING
          else "1500€ - 2500€",
          "published_at": timezone.now() - timedelta(days=random.randint(1, 30))
          if data["status"] == OfferStatus.PUBLISHED
          else None,
          "featured": random.choice([True, False]),
        },
      )
      if created:
        offer.causes.set([causes["Éducation"], causes["Jeunesse"]])
        offer.languages.set([languages["Français"], languages["Anglais"]])
        offer.skills.set([skills["Gestion de projet"], skills["Communication"]])
      offers.append(offer)
    return offers

  def seed_candidate(self, user, offers, countries, causes, skills):
    """
    Create (or update) the candidate's profile, desired position and
    applications so pages 8 & 9 have data to display and submit.
    """
    published = [o for o in offers if o.status == OfferStatus.PUBLISHED]

    profile, _ = CandidateProfile.objects.get_or_create(
      user=user,
      defaults={
        "first_name": "Amine",
        "last_name": "Benali",
        "bio": "Engagé dans l'éducation et la jeunesse depuis 5 ans.",
        "profile_completion": 80,
        "is_expert_profile": True,
        "actively_looking": True,
      },
    )

    desired = self.seed_desired_position(profile, countries, causes, skills)

    # Applications: one at each of several stages for the tracker demo.
    staged = [
      (ApplicationStage.INTERVIEW, published[0]),
      (ApplicationStage.PREQUALIFIED, published[1]),
      (ApplicationStage.SUBMITTED, published[2]),
    ]
    staged = [(stage, offer) for stage, offer in staged if offer]

    for stage, offer in staged:
      Application.objects.update_or_create(
        candidate=profile,
        offer=offer,
        defaults={"stage": stage},
      )

    self.stdout.write(
      self.style.SUCCESS(
        f"Candidate space seeded: {len(staged)} applications, "
        f"desired position ({desired.position_title})."
      )
    )
    return profile

  def seed_desired_position(self, profile, countries, causes, skills):
    """
    Create the candidate's 'Desired Position' fiche (page 9) with
    realistic values mapped to the backend enum/choices.
    """
    try:
      preferred_causes = [
        causes["Éducation"],
        causes["Jeunesse"],
      ]
      skills_leverage = [skills["Gestion de projet"], skills["Pédagogie"]]
      preferred_geo = [countries["DZA"]]
    except KeyError:
      preferred_causes = []
      skills_leverage = []
      preferred_geo = []

    desired, created = DesiredPosition.objects.get_or_create(
      candidate=profile,
      defaults={
        "position_title": "Chef de projet éducation",
        "engagement_types": ["volunteering", "salaried"],
        "modalities": ["on_site"],
        "availability": Availability.PART_TIME,
        "mobility": Mobility.NATIONAL,
        "position_level": PositionLevel.CONFIRMED,
        "min_daily_rate": None,
        "available_from": timezone.now() + timedelta(days=30),
        "email_alerts": True,
      },
    )
    desired.preferred_causes.set(preferred_causes)
    desired.skills_to_leverage.set(skills_leverage)
    desired.preferred_geographies.set(preferred_geo)
    return desired
