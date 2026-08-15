from django.urls import path

from .views import (
  CandidateRegisterView,
  CustomTokenObtainPairView,
  CustomTokenRefreshView,
  LogoutView,
  MeView,
  OrganizationRegisterView,
)

urlpatterns = [
  # JWT Authentication Routes
  path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
  path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
  path("logout/", LogoutView.as_view(), name="token_blacklist"),
  # user profile Route
  path("me/", MeView.as_view(), name="auth_me"),
  # registration Routes
  path(
    "register/candidate/",
    CandidateRegisterView.as_view(),
    name="register_candidate",
  ),
  path(
    "register/organization/",
    OrganizationRegisterView.as_view(),
    name="register_organization",
  ),
]
