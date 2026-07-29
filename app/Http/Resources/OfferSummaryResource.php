<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class OfferSummaryResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'uuid' => $this->uuid,
            'slug' => $this->slug,
            'title' => $this->title,
            'engagement_type' => [
                'value' => $this->engagement_type?->value ?? $this->engagement_type,
                'label' => $this->engagement_type_label,
            ],
            'employment_contract' => $this->employment_contract,
            'location' => [
                'country_code' => $this->country_code,
                'country' => $this->country?->name_fr,
                'region' => $this->region,
                'city' => $this->city,
                'label' => $this->location_label,
                'distance_km' => $this->when(isset($this->distance_km), fn () => round((float) $this->distance_km, 1)),
            ],
            'remote_mode' => [
                'value' => $this->remote_mode?->value ?? $this->remote_mode,
                'label' => $this->remote_mode_label,
            ],
            'duration_label' => $this->duration_label,
            'experience_level' => $this->experience_level,
            'featured' => (bool) $this->featured,
            'published_at' => $this->published_at?->toISOString(),
            'expires_at' => $this->expires_at?->toISOString(),
            'organization' => new OrganizationSummaryResource($this->whenLoaded('organization')),
            'causes' => CauseResource::collection($this->whenLoaded('causes')),
            'languages' => $this->whenLoaded('languages', fn () => $this->languages->map(fn ($language) => [
                'code' => $language->code,
                'name' => $language->name_fr,
            ])),
            'skills' => $this->whenLoaded('skills', fn () => $this->skills->map(fn ($skill) => [
                'id' => $skill->id,
                'name' => $skill->name,
                'slug' => $skill->slug,
                'required' => (bool) $skill->pivot?->is_required,
            ])),
        ];
    }
}
