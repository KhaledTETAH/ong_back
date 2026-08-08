from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.enums import Role
from apps.accounts.permissions import IsCandidate
from config.responses import SuccessResponse

from .models import (
  Country,
  Offer,
  OfferEvent,
  Organization,
  SavedOffer,
  SponsorshipMission,
  SponsorSlot,
)
from .serializers import (
  ApplicationSerializer,
  OfferCreateSerializer,
  OfferDetailSerializer,
  OfferSummarySerializer,
  OrganizationDetailSerializer,
  OrganizationSummarySerializer,
  ShareOfferSerializer,
  SponsorshipMissionReadSerializer,
  SponsorshipMissionSerializer,
)


def published_offers():
  return (
    Offer.objects.filter(status="published")
    .select_related("organization", "country", "organization__country")
    .prefetch_related(
      "causes",
      "languages",
      "skills",
      "organization__causes",
    )
  )


class HomeView(APIView):
  permission_classes = [AllowAny]

  def get(self, request):
    featured = published_offers().filter(featured=True)[:4]
    sponsor = (
      SponsorSlot.objects.filter(placement="homepage", is_active=True)
      .order_by("-starts_at")
      .first()
    )
    return SuccessResponse(
      {
        "stats": {
          "open_offers": published_offers().count(),
          "verified_organizations": Organization.objects.filter(
            is_active=True, verification_status__in=["verified", "certified_plus"]
          ).count(),
          "candidate_price": "100 %",
        },
        "featured_offers": OfferSummarySerializer(featured, many=True).data,
        "coverage_countries": list(
          Country.objects.filter(is_covered=True).values("code", "name_fr")
        ),
        "sponsor": {
          "sponsor_name": sponsor.sponsor_name,
          "label": sponsor.label,
          "copy": sponsor.copy,
          "target_url": sponsor.target_url,
        }
        if sponsor
        else None,
      },
      "Homepage data retrieved.",
    )


class OfferListView(APIView):
  permission_classes = [AllowAny]

  def get(self, request):
    qs = published_offers()
    q = request.query_params.get("q")
    if q:
      qs = qs.filter(
        Q(title__icontains=q)
        | Q(description__icontains=q)
        | Q(desired_profile__icontains=q)
        | Q(organization__name__icontains=q)
        | Q(skills__name__icontains=q)
        | Q(causes__name__icontains=q)
      ).distinct()
    if country := request.query_params.get("country"):
      qs = qs.filter(country_id=country.upper())
    if city := request.query_params.get("city"):
      qs = qs.filter(city__icontains=city)
    if offer_type := request.query_params.get("type"):
      qs = qs.filter(engagement_type=offer_type)
    if cause := request.query_params.get("cause"):
      qs = qs.filter(causes__slug=cause)
    if mode := request.query_params.get("mode"):
      qs = qs.filter(remote_mode=mode)
    if language := request.query_params.get("language"):
      qs = qs.filter(languages__code=language)
    if experience := request.query_params.get("experience_level"):
      qs = qs.filter(experience_level=experience)
    match request.query_params.get("duration"):
      case "short":
        qs = qs.filter(duration_days__lte=30)
      case "medium":
        qs = qs.filter(duration_days__gt=30, duration_days__lte=180)
      case "long":
        qs = qs.filter(Q(duration_days__gt=180) | Q(duration_days__isnull=True))
    if request.query_params.get("sort") == "oldest":
      qs = qs.order_by("published_at")
    elif request.query_params.get("sort") == "recent":
      qs = qs.order_by("-published_at")
    return SuccessResponse(
      OfferSummarySerializer(qs.distinct(), many=True).data, "Offers retrieved."
    )


class OfferDetailView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, slug):
    offer = get_object_or_404(published_offers(), slug=slug)
    Offer.objects.filter(pk=offer.pk).update(views_count=offer.views_count + 1)
    offer.refresh_from_db()
    return SuccessResponse(
      OfferDetailSerializer(offer, context={"request": request}).data,
      "Offer retrieved.",
    )


class SimilarOffersView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, slug):
    offer = get_object_or_404(Offer, slug=slug)
    cause_ids = offer.causes.values_list("id", flat=True)
    offers = (
      published_offers()
      .exclude(pk=offer.pk)
      .filter(Q(engagement_type=offer.engagement_type) | Q(causes__id__in=cause_ids))
      .distinct()[:6]
    )
    return SuccessResponse(
      OfferSummarySerializer(offers, many=True).data, "Similar offers retrieved."
    )


class ShareOfferView(APIView):
  permission_classes = [AllowAny]

  def post(self, request, slug):
    offer = get_object_or_404(Offer, slug=slug, status="published")
    serializer = ShareOfferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    OfferEvent.objects.create(
      offer=offer,
      user=request.user if request.user.is_authenticated else None,
      event_type="share",
      channel=serializer.validated_data["channel"],
      ip_hash=OfferEvent.digest(request.META.get("REMOTE_ADDR")),
      user_agent_hash=OfferEvent.digest(request.META.get("HTTP_USER_AGENT")),
    )
    return SuccessResponse(None, "Share event recorded.")


class ApplyOfferView(APIView):
  permission_classes = [IsAuthenticated, IsCandidate]

  def post(self, request, slug):
    offer = get_object_or_404(Offer, slug=slug, status="published")
    serializer = ApplicationSerializer(
      data=request.data, context={"request": request, "offer": offer}
    )
    serializer.is_valid(raise_exception=True)
    application = serializer.save()
    return SuccessResponse(
      {
        "id": application.id,
        "status": application.status,
        "applied_at": application.applied_at,
      },
      "Application submitted.",
      status=status.HTTP_201_CREATED,
    )


class SaveOfferView(APIView):
  permission_classes = [IsAuthenticated, IsCandidate]

  def put(self, request, slug):
    offer = get_object_or_404(Offer, slug=slug, status="published")
    SavedOffer.objects.get_or_create(user=request.user, offer=offer)
    return SuccessResponse(None, "Offer saved.")

  def delete(self, request, slug):
    offer = get_object_or_404(Offer, slug=slug)
    SavedOffer.objects.filter(user=request.user, offer=offer).delete()
    return SuccessResponse(None, "Offer removed from saved list.")


class OrganizationListView(APIView):
  permission_classes = [AllowAny]

  def get(self, request):
    qs = (
      Organization.objects.filter(is_active=True)
      .select_related("country")
      .prefetch_related("causes")
      .annotate(open_offers_count=Count("offers", filter=Q(offers__status="published")))
    )
    if q := request.query_params.get("q"):
      qs = qs.filter(
        Q(name__icontains=q)
        | Q(description__icontains=q)
        | Q(mission__icontains=q)
        | Q(city__icontains=q)
      )
    if country := request.query_params.get("country"):
      qs = qs.filter(country_id=country.upper())
    if cause := request.query_params.get("cause"):
      qs = qs.filter(causes__slug=cause)
    if verification := request.query_params.get("verification"):
      qs = qs.filter(verification_status=verification)
    if org_type := request.query_params.get("type"):
      qs = qs.filter(type=org_type)
    if size := request.query_params.get("size"):
      qs = qs.filter(size=size)
    if request.query_params.get("sort") == "offers":
      qs = qs.order_by("-open_offers_count", "name")
    elif request.query_params.get("sort") == "name":
      qs = qs.order_by("name")
    return SuccessResponse(
      OrganizationSummarySerializer(qs.distinct(), many=True).data,
      "Organizations retrieved.",
    )


class OrganizationDetailView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, slug):
    organization = get_object_or_404(
      Organization.objects.filter(is_active=True)
      .select_related("country")
      .prefetch_related(
        "causes",
        "offers__country",
        "offers__causes",
        "offers__languages",
        "offers__skills",
      ),
      slug=slug,
    )
    organization.open_offers_count = organization.offers.filter(
      status="published"
    ).count()
    return SuccessResponse(
      OrganizationDetailSerializer(organization).data, "Organization retrieved."
    )


class OrganizationOfferCreateView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, slug):
    organization = get_object_or_404(Organization.objects.select_related("country"), slug=slug)
    if request.user != organization.owner and request.user.role not in {
      Role.ADMIN,
      Role.MODERATOR,
    }:
      raise PermissionDenied("You are not allowed to create offers for this organization.")

    serializer = OfferCreateSerializer(
      data=request.data,
      context={"request": request, "organization": organization},
    )
    serializer.is_valid(raise_exception=True)
    offer = serializer.save()
    return SuccessResponse(
      OfferSummarySerializer(offer, context={"request": request}).data,
      "Offer created.",
      status=status.HTTP_201_CREATED,
    )


class SponsorshipMissionCreateView(APIView):
  permission_classes = [AllowAny]

  def post(self, request):
    serializer = SponsorshipMissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mission = serializer.save()
    data = SponsorshipMissionReadSerializer(mission).data
    data["debug_verification_token"] = mission.debug_verification_token
    return SuccessResponse(
      data, "Sponsorship mission created.", status=status.HTTP_201_CREATED
    )


class SponsorshipMissionDetailView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, tracking_uuid):
    mission = get_object_or_404(
      SponsorshipMission.objects.prefetch_related("causes"), tracking_uuid=tracking_uuid
    )
    if not mission.token_matches(request.query_params.get("token", "")):
      raise PermissionDenied("Invalid tracking token.")
    return SuccessResponse(
      SponsorshipMissionReadSerializer(mission).data, "Sponsorship mission retrieved."
    )

  def post(self, request, tracking_uuid):
    mission = get_object_or_404(
      SponsorshipMission.objects.prefetch_related("causes"), tracking_uuid=tracking_uuid
    )
    if not mission.verify(request.data.get("token", "")):
      raise PermissionDenied("Invalid verification token.")
    return SuccessResponse(
      SponsorshipMissionReadSerializer(mission).data, "Sponsorship mission verified."
    )



class MatchingOffersAPIView(APIView):

  permission_classes = [IsAuthenticated]

  def get(self, request):

    desired = request.user.desired_position

    results = OfferMatcher().get_matching_offers(desired)

    serializer = MatchingOfferSerializer(
        results,
        many=True
    )

    return Response(serializer.data)


#already done in OrganizationListView
""" class OfferSearchAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        queryset = (
            Offer.objects.filter(
                status=OfferStatus.PUBLISHED,
            )
            .select_related(
                "organization",
                "country",
            )
            .prefetch_related(
                "skills",
                "causes",
                "languages",
            )
            .distinct()
        )

        q = request.query_params.get("q")

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(desired_profile__icontains=q)
                | Q(responsibilities__icontains=q)
                | Q(organization__name__icontains=q)
            )
        country = request.query_params.get("country")

        if country:
            queryset = queryset.filter(
                country_id=country.upper()
            )

        city = request.query_params.get("city")

        if city:
            queryset = queryset.filter(
                city__icontains=city
            )
        serializer = OfferSummarySerializer(
            queryset,
            many=True,
        )

        return SuccessResponse(
            serializer.data,
            "Offers retrieved successfully.",
        )         """
