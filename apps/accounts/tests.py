from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .enums import Role, Status

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
    self.public_page7_url = reverse("public_page7")
    self.protected_page89_url = reverse("protected_page89")
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

    # tokens are inside the "data" dictionary
    self.assertIn("access", response.data["data"])
    self.assertIn("refresh", response.data["data"])

    # save token for subsequent tests
    self.access_token = response.data["data"]["access"]

  def test_02_login_invalid_credentials(self):
    """
    Test: POST /api/v1/auth/token/ with wrong password returns 401.
    """
    payload = {"email": "test@example.com", "password": "wrongpassword"}
    response = self.client.post(self.token_url, payload, format="json")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_03_public_page7_no_token(self):
    """
    Test: GET /api/v1/public-page7/ returns 200 OK without authentication.
    """
    response = self.client.get(self.public_page7_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # assert SuccessResponse structure
    self.assertTrue(response.data["success"])
    self.assertIn("message", response.data["data"])

  def test_04_protected_page89_no_token(self):
    """
    Test: GET /api/v1/protected-page89/ returns 401 Unauthorized without a token.
    """
    response = self.client.get(self.protected_page89_url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_05_protected_page89_with_token(self):
    """
    Test: GET /api/v1/protected-page89/ returns 200 OK with a valid Bearer token.
    """
    # get a valid token (which is wrapped in SuccessResponse)
    login_response = self.client.post(
      self.token_url,
      {"email": "test@example.com", "password": "securepassword123"},
      format="json",
    )

    # extract from the "data" key
    token = login_response.data["data"]["access"]

    # set the Authorization header
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # test the protected endpoint
    response = self.client.get(self.protected_page89_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # assert SuccessResponse structure
    self.assertTrue(response.data["success"])
    self.assertIn("message", response.data["data"])

  def test_06_me_endpoint_with_token(self):
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
