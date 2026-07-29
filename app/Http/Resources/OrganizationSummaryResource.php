<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class OrganizationSummaryResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'slug' => $this->slug,
            'type' => $this->type,
            'location' => [
                'country_code' => $this->country_code,
                'country' => $this->whenLoaded('country', fn () => $this->country?->name_fr),
                'city' => $this->city,
            ],
            'description' => $this->description,
            'verification' => [
                'status' => $this->verification_status?->value ?? $this->verification_status,
                'label' => $this->verification_label,
            ],
            'logo_url' => $this->logo_url,
            'causes' => CauseResource::collection($this->whenLoaded('causes')),
            'open_offers_count' => $this->when(isset($this->offers_count), $this->offers_count),
        ];
    }
}
