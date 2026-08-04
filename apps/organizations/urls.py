from django.urls import path
from .views import OrganizationListView, OrganizationDetailView

urlpatterns = [
  # GET all active organizations
  path("", OrganizationListView.as_view(), name="organization_list"),
  # GET a single active organization by UUID
  path("<uuid:id>/", OrganizationDetailView.as_view(), name="organization_detail"),
]
