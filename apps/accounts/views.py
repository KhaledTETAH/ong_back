from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import LogoutSerializer
from config.responses import SuccessResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .permissions import IsCandidate


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

  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    return SuccessResponse(
      data=response.data, message="Login successful.", status=response.status_code
    )


class CustomTokenRefreshView(TokenRefreshView):
  """
  Wraps the default SimpleJWT refresh view.
  """

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
