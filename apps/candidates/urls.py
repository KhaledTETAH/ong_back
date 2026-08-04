from django.urls import path

from .views import ActivelyLookingView, DesiredPositionView

app_name = "candidates"

urlpatterns = [
  # GET /api/me/desired-position/
  # PUT/PATCH /api/me/desired-position/
  path("desired-position/", DesiredPositionView.as_view(), name="desired_position"),
  # PATCH /api/me/actively-looking/
  path("actively-looking/", ActivelyLookingView.as_view(), name="actively_looking"),
]
