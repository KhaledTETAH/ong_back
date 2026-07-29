from django.urls import path
from .views import MeView, PublicPage7View, ProtectedPage89View, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
	# JWT Authentication Routes
	path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
	path('logout/', LogoutView.as_view(), name='token_blacklist'),
	
	# user profile Route
	path('me/', MeView.as_view(), name='auth_me'),
	
	# testing Routes (Page 7 vs Page 8/9)
	path('public-page7/', PublicPage7View.as_view(), name='public_page7'),
	path('protected-page89/', ProtectedPage89View.as_view(), name='protected_page89'),
]