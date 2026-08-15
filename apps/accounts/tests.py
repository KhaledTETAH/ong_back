from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .enums import Role, Status
from .serializers import (
  CandidateRegistrationSerializer,
  OrganizationRegistrationSerializer,
)

User = get_user_model()


class RBACAndAuthTests(TestCase):
  def setUp(self):
    """
    Set up test client and a test user before each test.
    """
    self.client = APIClient()

    self.user = User.objects.create_user(
      email="test@example.com",
      password="securepassword123",
      role=Role.CANDIDATE,
      status=Status.ACTIVE,
      email_verified=True,
    )

    self.token_url = reverse("token_obtain_pair")
    self.me_url = reverse("auth_me")

  def test_01_login_success(self):
    """
    Test: POST /api/v1/auth/token/ returns 200 OK wrapped in SuccessResponse.
    """
    payload = {"email": "test@example.com", "password": "securepassword123"}
    response = self.client.post(self.token_url, payload, format="json")

    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # assert SuccessResponse structure
    self.assertTrue(response.data["success"])
    self.assertEqual(response.data["status_code"], 200)

    # access token is in the body, refresh token only in an httpOnly cookie
    self.assertIn("access", response.data["data"])
    self.assertNotIn("refresh", response.data["data"])
    cookie_name = django_settings.AUTH_COOKIE
    self.assertIn(cookie_name, response.cookies)
    self.assertTrue(response.cookies[cookie_name]["httponly"])

    # save token for subsequent tests
    self.access_token = response.data["data"]["access"]

  def test_02_login_invalid_credentials(self):
    """
    Test: POST /api/v1/auth/token/ with wrong password returns 401.
    """
    payload = {"email": "test@example.com", "password": "wrongpassword"}
    response = self.client.post(self.token_url, payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_03_me_endpoint_requires_auth(self):
    """
    Test: GET /api/v1/auth/me/ returns 401 Unauthorized without a token.
    """
    response = self.client.get(self.me_url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_04_me_endpoint_with_token(self):
    """
    Test: GET /api/v1/auth/me/ returns 200 OK with user role and status.
    """
    # get a valid token
    login_response = self.client.post(
      self.token_url,
      {"email": "test@example.com", "password": "securepassword123"},
      format="json",
    )
    token = login_response.data["data"]["access"]

    # set the Authorization header
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # test the /me/ endpoint
    response = self.client.get(self.me_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # extract the nested 'data' dictionary from SuccessResponse
    user_data = response.data["data"]

    self.assertEqual(user_data["email"], "test@example.com")
    self.assertEqual(user_data["role"], Role.CANDIDATE)
    self.assertEqual(user_data["status"], Status.ACTIVE)
    self.assertEqual(user_data["email_verified"], True)
    self.assertIn("id", user_data)

  def test_07_me_endpoint_no_token(self):
    """
    Test: GET /api/v1/auth/me/ returns 401 Unauthorized without a token.
    """
    response = self.client.get(self.me_url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordValidationTests(TestCase):
  """
  Tests ensuring Django's AUTH_PASSWORD_VALIDATORS are enforced on registration.
  """

  def test_candidate_registration_rejects_common_password(self):
    """
    Test: candidate registration rejects a common/weak 8+ char password.
    """
    serializer = CandidateRegistrationSerializer(
      data={"email": "new.candidate@example.com", "password": "password1"}
    )
    self.assertFalse(serializer.is_valid())
    self.assertIn("non_field_errors", serializer.errors)

  def test_organization_registration_rejects_numeric_password(self):
    """
    Test: organization registration rejects an all-numeric password.
    """
    serializer = OrganizationRegistrationSerializer(
      data={
        "owner_email": "org.owner@example.com",
        "password": "12345678",
        "organization_name": "Test Org",
        "organization_type": "association",
        "country_code": "DZ",
        "city": "Oran",
        "registry_number": "",
        "description": "desc",
        "mission": "",
      }
    )
    self.assertFalse(serializer.is_valid())
    self.assertIn("non_field_errors", serializer.errors)

  def test_candidate_registration_accepts_strong_password(self):
    """
    Test: candidate registration accepts a strong password.
    """
    serializer = CandidateRegistrationSerializer(
      data={
        "email": "strong.candidate@example.com",
        "password": "Tr0ub4dour&wonderful",
      }
    )
    self.assertTrue(serializer.is_valid())


class CookieAuthTests(TestCase):
  """
  Tests that the refresh token is stored in an httpOnly cookie and is used
  for refresh/logout instead of being exposed in the response body.
  """

  def setUp(self):
    """
    Create a candidate and the login URL.
    """
    self.user = get_user_model().objects.create_user(
      email="cookie@example.com",
      password="securepassword123",
      role=Role.CANDIDATE,
      status=Status.ACTIVE,
      email_verified=True,
    )
    self.client = APIClient()
    self.cookie_name = django_settings.AUTH_COOKIE
    self.login_url = reverse("token_obtain_pair")
    self.refresh_url = reverse("token_refresh")
    self.logout_url = reverse("token_blacklist")

  def _login(self):
    """
    Helper: login and assert the refresh cookie is set and no refresh token
    is exposed in the body.
    """
    response = self.client.post(
      self.login_url,
      {"email": "cookie@example.com", "password": "securepassword123"},
      format="json",
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["success"], True)
    self.assertIn("access", response.data["data"])
    self.assertNotIn("refresh", response.data["data"])
    self.assertIn(self.cookie_name, response.cookies)
    self.assertTrue(response.cookies[self.cookie_name]["httponly"])
    return response.data["data"]["access"]

  def test_login_sets_httponly_refresh_cookie(self):
    """
    Test: login issues an access token in the body and a refresh cookie.
    """
    self._login()

  def test_refresh_uses_cookie_and_rotates(self):
    """
    Test: refresh with the cookie returns a new access token and rotates the
    refresh token, blacklisting the previous one.
    """
    self._login()
    first_cookie = self.client.cookies[self.cookie_name].value

    response = self.client.post(self.refresh_url, {}, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("access", response.data["data"])
    self.assertNotIn("refresh", response.data["data"])

    # Rotation issued a new refresh cookie.
    new_cookie = self.client.cookies[self.cookie_name].value
    self.assertNotEqual(first_cookie, new_cookie)

  def test_refresh_rejects_blacklisted_token(self):
    """
    Test: an old refresh token cannot be reused after rotation.
    """
    self._login()
    first_refresh = self.client.cookies[self.cookie_name].value

    # Rotate once (blacklists the first refresh token).
    self.client.post(self.refresh_url, {}, format="json")

    # Trying to refresh with the stale token fails.
    client = APIClient()
    client.cookies[self.cookie_name] = first_refresh
    response = client.post(self.refresh_url, {}, format="json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_logout_clears_cookie(self):
    """
    Test: logout removes the refresh cookie.
    """
    access = self._login()
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    response = self.client.post(self.logout_url, {}, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn(self.cookie_name, response.cookies)
    self.assertEqual(response.cookies[self.cookie_name]["max-age"], 0)
