<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class SponsorshipMissionResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'tracking_uuid' => $this->tracking_uuid,
            'contact_email' => $this->contact_email,
            'company_name' => $this->company_name,
            'company_legal_id' => $this->company_legal_id,
            'country_code' => $this->country_code,
            'region' => $this->region,
            'title' => $this->title,
            'description' => $this->description,
            'objectives' => $this->objectives,
            'deliverables' => $this->deliverables,
            'required_profiles' => $this->required_profiles,
            'man_days' => $this->man_days,
            'visibility' => $this->visibility?->value ?? $this->visibility,
            'status' => $this->status?->value ?? $this->status,
            'verified_email_at' => $this->verified_email_at?->toISOString(),
            'causes' => CauseResource::collection($this->whenLoaded('causes')),
            'created_at' => $this->created_at?->toISOString(),
        ];
    }
}
