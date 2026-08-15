from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from config.responses import SuccessResponse

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationListView(APIView):
  """
  GET /api/organizations/
  Returns a list of all active organizations.
  """

  permission_classes = [AllowAny]

  def get(self, request):
    organizations = (
      Organization.objects.filter(is_active=True)
      .select_related("country")
      .prefetch_related("causes")
      .annotate(open_offers_count=Count("offers", filter=Q(offers__status="published")))
    )

    serializer = OrganizationSerializer(organizations, many=True)

    return SuccessResponse(
      data=serializer.data, message="Organizations retrieved successfully"
    )


class OrganizationDetailView(APIView):
  """
  GET /api/organizations/<slug>/
  Returns details of a single active organization.
  """

  permission_classes = [AllowAny]

  def get(self, request, slug):
    organization = get_object_or_404(
      Organization.objects.filter(is_active=True)
      .prefetch_related("offers", "causes")
      .annotate(
        open_offers_count=Count("offers", filter=Q(offers__status="published"))
      ),
      slug=slug,
    )

    serializer = OrganizationSerializer(organization)

    return SuccessResponse(
      data=serializer.data, message="Organization retrieved successfully"
    )
