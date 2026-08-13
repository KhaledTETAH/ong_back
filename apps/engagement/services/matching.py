class OfferMatcher:

    def match(self, desired_position, offer):
        score = 0

        if offer.engagement_type in desired_position.engagement_types.all():
            score += 20

        if offer.country == desired_position.country:
            score += 15

        if offer.causes.filter(
            id__in=desired_position.preferred_causes.values_list("id", flat=True)
        ).exists():
            score += 20

        common_skills = offer.skills.filter(
            id__in=desired_position.highlighted_skills.values_list(
                "id",
                flat=True
            )
        ).count()

        score += common_skills * 5

        return min(score, 100)
    def get_matching_offers(desired_position):

    offers = Offer.objects.filter(
        status=OfferStatus.PUBLISHED
    )

    results = []

    matcher = OfferMatcher()

    for offer in offers:
        score = matcher.match(desired_position, offer)

        results.append({
            "offer": offer,
            "score": score
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )    