from django.urls import path

from .views import (
  ApplyOfferView,
  HomeView,
  OfferDetailView,
  OfferListView,
  OrganizationDetailView,
  OrganizationListView,
  OrganizationOfferCreateView,
  SaveOfferView,
  ShareOfferView,
  SimilarOffersView,
  SponsorshipMissionCreateView,
  SponsorshipMissionDetailView,
  MatchingOffersAPIView,

)

urlpatterns = [
  path("home/", HomeView.as_view(), name="home"),
  path("offers/", OfferListView.as_view(), name="offers"),
  path("offers/<slug:slug>/", OfferDetailView.as_view(), name="offer_detail"),
  path(
    "offers/<slug:slug>/similar/", SimilarOffersView.as_view(), name="offer_similar"
  ),
  path("offers/<slug:slug>/share/", ShareOfferView.as_view(), name="offer_share"),
  path(
    "offers/<slug:slug>/applications/", ApplyOfferView.as_view(), name="offer_apply"
  ),
  path("offers/<slug:slug>/saved/", SaveOfferView.as_view(), name="offer_saved"),
  path("organizations/", OrganizationListView.as_view(), name="organizations"),
  path(
    "organizations/<slug:slug>/offers/",
    OrganizationOfferCreateView.as_view(),
    name="organization_offer_create",
  ),
  path(
    "organizations/<slug:slug>/",
    OrganizationDetailView.as_view(),
    name="organization_detail",
  ),
  path(
    "sponsorship-missions/",
    SponsorshipMissionCreateView.as_view(),
    name="sponsorship_create",
  ),
  path(
    "sponsorship-missions/<uuid:tracking_uuid>/",
    SponsorshipMissionDetailView.as_view(),
    name="sponsorship_detail",
  ),
  path(
    "sponsorship-missions/<uuid:tracking_uuid>/verify/",
    SponsorshipMissionDetailView.as_view(),
    name="sponsorship_verify",
  ),
     path(
        "offers/matching/",
        MatchingOffersAPIView.as_view(),
        name="matching-offers"
    ),
   
]
