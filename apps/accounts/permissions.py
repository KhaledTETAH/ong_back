from rest_framework.permissions import BasePermission


class IsCandidate(BasePermission):
  """
  Grants access only to authenticated users with the candidate role.
  """

  def has_permission(self, request, view):
    return bool(
      request.user
      and request.user.is_authenticated
      and request.user.role == "candidate"
    )


class IsNGOMember(BasePermission):
  """
  Grants access only to authenticated users with the NGO member role.
  """

  def has_permission(self, request, view):
    return bool(
      request.user
      and request.user.is_authenticated
      and request.user.role == "ngo_member"
    )
