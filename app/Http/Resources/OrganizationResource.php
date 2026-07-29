<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;

class OrganizationResource extends OrganizationSummaryResource
{
    public function toArray(Request $request): array
    {
        return [
            ...parent::toArray($request),
            'registry_number' => $this->registry_number,
            'size' => $this->size,
            'mission' => $this->mission,
            'website' => $this->website,
            'founded_year' => $this->founded_year,
            'volunteer_count' => $this->volunteer_count,
            'offers' => OfferSummaryResource::collection($this->whenLoaded('offers')),
            'created_at' => $this->created_at?->toISOString(),
        ];
    }
}
