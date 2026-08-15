from django.urls import path

from .views import OrganizationDetailView, OrganizationListView

urlpatterns = [
  # GET all active organizations
  path("", OrganizationListView.as_view(), name="organization_list"),
  # GET a single active organization by slug
  path("<slug:slug>/", OrganizationDetailView.as_view(), name="organization_detail"),
]
