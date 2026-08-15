from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.responses import SuccessResponse

from .permissions import IsCandidate
from .serializers import (
  CandidateRegistrationSerializer,
  LogoutSerializer,
  OrganizationRegistrationSerializer,
)


class MeView(APIView):
  """
  Returns the current authenticated user's role and status.
  """

  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user

    user_data = {
      "id": str(user.id),
      "email": user.email,
      "role": user.role,
      "status": user.status,
      "email_verified": user.email_verified,
    }

    return SuccessResponse(user_data, "Profile retrieved successfully.")


class CandidateRegisterView(CreateAPIView):
  """
  POST /api/v1/auth/register/candidate/
  Creates a candidate user account.
  """

  permission_classes = [AllowAny]
  serializer_class = CandidateRegistrationSerializer
  throttle_classes = [ScopedRateThrottle]
  throttle_scope = "register"

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return SuccessResponse(
      data={
        "id": str(user.id),
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "email_verified": user.email_verified,
      },
      message="Candidate account created successfully.",
      status=201,
    )


class OrganizationRegisterView(CreateAPIView):
  """
  POST /api/v1/auth/register/organization/
  Creates an organization owner user and the organization record.
  """

  permission_classes = [AllowAny]
  serializer_class = OrganizationRegistrationSerializer
  throttle_classes = [ScopedRateThrottle]
  throttle_scope = "register"

  def create(self, request, *args, **kwargs):
    from apps.core.models import Country
    from apps.organizations.enums import VerificationStatus
    from apps.organizations.models import Organization

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    owner = get_user_model().objects.create_user(
      email=data["owner_email"],
      password=data["password"],
      role="ngo_member",
      status="active",
    )

    country, _ = Country.objects.get_or_create(
      code=data["country_code"].upper(),
      defaults={"name": data["country_code"].upper()},
    )

    organization = Organization.objects.create(
      owner=owner,
      name=data["organization_name"],
      type=data["organization_type"],
      country=country,
      city=data["city"],
      registry_number=data["registry_number"],
      description=data["description"],
      mission=data.get("mission", ""),
      is_active=True,
      verification_status=VerificationStatus.IN_PROGRESS,
    )

    return SuccessResponse(
      data={
        "id": str(organization.id),
        "name": organization.name,
        "slug": organization.slug,
      },
      message="Organization account created successfully.",
      status=201,
    )


class LogoutView(APIView):
  """
  POST /api/v1/auth/logout/
  Blacklists refresh token to preven reuse
  """

  permission_classes = [IsAuthenticated]
  serializer_class = LogoutSerializer

  def post(self, request):
    try:
      refresh_token = request.data.get("refresh")
      if not refresh_token:
        raise ValidationError({"refresh": "This field is required."})

      token = RefreshToken(refresh_token)
      token.blacklist()
    except TokenError:
      raise ValidationError({"refresh": "Token is invalid or already blacklisted"})

    return SuccessResponse(
      data=None,
      message="Logout Successful.",
    )


class CustomTokenObtainPairView(TokenObtainPairView):
  """
  Wraps the default SimpleJWT login view to return our standardized success format.
  """

  throttle_classes = [ScopedRateThrottle]
  throttle_scope = "login"

  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    return SuccessResponse(
      data=response.data, message="Login successful.", status=response.status_code
    )


class CustomTokenRefreshView(TokenRefreshView):
  """
  Wraps the default SimpleJWT refresh view.
  """

  throttle_classes = [ScopedRateThrottle]
  throttle_scope = "login"

  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    return SuccessResponse(
      data=response.data,
      message="Token refreshed successfully.",
      status=response.status_code,
    )


# mock views for Testing Page 7 vs Page 8/9


class PublicPage7View(APIView):
  """
  Simulates Page 7 (Public endpoints). Unauthenticated GET succeeds.
  """

  permission_classes = [AllowAny]

  def get(self, request):
    return SuccessResponse(
      data={"message": "Public data accessible to everyone (Page 7)"}
    )


class ProtectedPage89View(APIView):
  """
  Simulates Page 8/9 (Candidate-only endpoints). Unauthenticated GET returns 401.
  """

  permission_classes = [IsAuthenticated, IsCandidate]

  def get(self, request):
    return SuccessResponse(
      data={"message": f"Protected data for {request.user.role} (Page 8/9)"}
    )
