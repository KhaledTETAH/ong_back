<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;

class OfferResource extends OfferSummaryResource
{
    public function toArray(Request $request): array
    {
        return [
            ...parent::toArray($request),
            'description' => $this->description,
            'responsibilities' => $this->responsibilities,
            'desired_profile' => $this->desired_profile,
            'conditions' => $this->conditions,
            'start_date' => $this->start_date?->toDateString(),
            'end_date' => $this->end_date?->toDateString(),
            'contact_email' => $this->when(
                $request->user()?->role?->value === 'platform_admin',
                $this->contact_email
            ),
            'views_count' => $this->views_count,
            'is_saved' => $this->when(
                $request->user(),
                fn () => $this->savedBy()->where('user_id', $request->user()->id)->exists()
            ),
            'has_applied' => $this->when(
                $request->user()?->isCandidate(),
                fn () => $this->applications()->where('candidate_id', $request->user()->id)->exists()
            ),
        ];
    }
}
