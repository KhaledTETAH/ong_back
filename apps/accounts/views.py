from django.conf import settings
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

from .serializers import (
  CandidateRegistrationSerializer,
  LogoutSerializer,
  OrganizationRegistrationSerializer,
)


def _set_refresh_cookie(response, refresh):
  """
  Store the refresh token in an httpOnly cookie on the given response.
  """
  response.set_cookie(
    key=settings.AUTH_COOKIE,
    value=refresh,
    max_age=settings.AUTH_COOKIE_MAX_AGE,
    httponly=settings.AUTH_COOKIE_HTTPONLY,
    secure=settings.AUTH_COOKIE_SECURE,
    samesite=settings.AUTH_COOKIE_SAMESITE,
    path=settings.AUTH_COOKIE_PATH,
  )
  return response


def _clear_refresh_cookie(response):
  """
  Remove the refresh token cookie from the given response.
  """
  response.delete_cookie(
    key=settings.AUTH_COOKIE,
    path=settings.AUTH_COOKIE_PATH,
    samesite=settings.AUTH_COOKIE_SAMESITE,
  )
  return response


class MeView(APIView):
  """
  Returns the current authenticated user's role and status.
  """

  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user
    profile = getattr(user, "candidate_profile", None)

    user_data = {
      "id": str(user.id),
      "email": user.email,
      "role": user.role,
      "status": user.status,
      "email_verified": user.email_verified,
      "first_name": profile.first_name if profile else "",
      "last_name": profile.last_name if profile else "",
      "phone": user.phone or "",
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
  Blacklists the refresh token and clears the httpOnly refresh cookie.
  """

  permission_classes = [IsAuthenticated]
  serializer_class = LogoutSerializer

  def post(self, request):
    refresh_token = request.COOKIES.get(settings.AUTH_COOKIE) or request.data.get(
      "refresh"
    )
    if refresh_token:
      try:
        RefreshToken(refresh_token).blacklist()
      except TokenError:
        pass

    response = SuccessResponse(data=None, message="Logout Successful.")
    _clear_refresh_cookie(response)
    return response


class CustomTokenObtainPairView(TokenObtainPairView):
  """
  Login. Returns an access token in the body and stores the refresh token
  in an httpOnly cookie.
  """

  throttle_classes = [ScopedRateThrottle]
  throttle_scope = "login"

  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    if response.status_code != 200:
      return response

    refresh = response.data.get("refresh")
    payload = {"access": response.data["access"]}
    built = SuccessResponse(
      data=payload, message="Login successful.", status=response.status_code
    )
    if refresh:
      _set_refresh_cookie(built, refresh)
    return built


class CustomTokenRefreshView(TokenRefreshView):
  """
  Rotates the refresh token from the httpOnly cookie and returns a new access
  token in the body.
  """

  throttle_classes = [ScopedRateThrottle]
  throttle_scope = "refresh"

  def post(self, request, *args, **kwargs):
    refresh = request.COOKIES.get(settings.AUTH_COOKIE) or request.data.get("refresh")
    if not refresh:
      raise ValidationError({"refresh": "This field is required."})

    try:
      token = RefreshToken(refresh)
      access = str(token.access_token)
      if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]:
        token.set_jti()
        token.set_exp()
        token.set_iat()
      new_refresh = str(token)
      if settings.SIMPLE_JWT["BLACKLIST_AFTER_ROTATION"]:
        try:
          RefreshToken(refresh).blacklist()
        except (TokenError, AttributeError):
          pass
    except TokenError:
      raise ValidationError({"refresh": "Token is invalid or expired"})

    response = SuccessResponse(
      data={"access": access}, message="Token refreshed successfully."
    )
    _set_refresh_cookie(response, new_refresh)
    return response
