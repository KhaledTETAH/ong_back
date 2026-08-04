from rest_framework import generics
from rest_framework.views import APIView

from config.responses import SuccessResponse

from .models import CandidateProfile, DesiredPosition
from .serializers import ActivelyLookingSerializer, DesiredPositionSerializer


class DesiredPositionView(generics.RetrieveUpdateAPIView):
  """
  GET: Retrieve the candidate's desired position.
  PUT/PATCH: Update the desired position.
  (Auto-creates the profile and desired position if they don't exist yet).
  """

  serializer_class = DesiredPositionSerializer

  def get_object(self):
    # ensure the base CandidateProfile exists for this user
    profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)

    # get or create the DesiredPosition linked to that profile
    obj, created = DesiredPosition.objects.get_or_create(candidate=profile)
    return obj

  def update(self, request, *args, **kwargs):

    # override default DRF update to wrap in SuccessResponse
    partial = kwargs.pop("partial", False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    return SuccessResponse(
      data=serializer.data, message="Desired position updated successfully."
    )

  def retrieve(self, request, *args, **kwargs):
    # override default DRF retrieve to wrap in SuccessResponse
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    return SuccessResponse(
      data=serializer.data, message="Desired position retrieved successfully."
    )


class ActivelyLookingView(APIView):
  """
  PATCH: Lightweight endpoint to toggle the "Actively Looking" boolean.
  """

  def patch(self, request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)

    serializer = ActivelyLookingSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return SuccessResponse(
      data=serializer.data, message="Actively looking status updated."
    )
