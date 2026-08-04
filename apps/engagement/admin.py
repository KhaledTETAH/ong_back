from django.contrib import admin

from .models import (
  Cause,
  Country,
  Language,
  Offer,
  Organization,
  Skill,
  SponsorshipMission,
)

admin.site.register(Country)
admin.site.register(Cause)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Organization)
admin.site.register(Offer)
admin.site.register(SponsorshipMission)
