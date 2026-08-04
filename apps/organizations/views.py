from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Organization
from .serializers import OrganizationSerializer
from config.responses import SuccessResponse
from rest_framework.permissions import AllowAny


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
    )

    serializer = OrganizationSerializer(organizations, many=True)

    return SuccessResponse(
      data=serializer.data, message="Organizations retrieved successfully"
    )


class OrganizationDetailView(APIView):
  """
  GET /api/organizations/<uuid:id>/
  Returns details of a single active organization.
  """

  permission_classes = [AllowAny]

  def get(self, request, id):
    organization = get_object_or_404(
      Organization.objects.filter(is_active=True).prefetch_related("offers", "causes"),
      id=id,
    )

    serializer = OrganizationSerializer(organization)

    return SuccessResponse(
      data=serializer.data, message="Organization retrieved successfully"
    )
