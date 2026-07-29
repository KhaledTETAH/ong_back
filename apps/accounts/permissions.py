from rest_framework.permissions import BasePermission

class IsCandidate(BasePermission):
	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.role == 'candidate')
	
class IsNGOMember(BasePermission):
	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.role == 'ngo_member')
