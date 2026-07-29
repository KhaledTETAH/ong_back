<?php

namespace App\Services;

use App\Models\Country;
use App\Models\Offer;
use App\Models\Organization;
use App\Models\SponsorSlot;
use Illuminate\Support\Facades\Cache;

class HomepageService
{
    public function data(): array
    {
        return Cache::remember('public.homepage.v1', now()->addMinutes(10), function (): array {
            return [
                'stats' => [
                    'open_offers' => Offer::published()->count(),
                    'verified_organizations' => Organization::publiclyVisible()->count(),
                    'candidate_price' => '100 %',
                ],
                'featured_offers' => Offer::published()
                    ->with([
                        'organization:id,name,slug,type,country_code,city,description,verification_status,logo_path',
                        'organization.country:code,name_fr',
                        'country:code,name_fr',
                        'causes:id,name,slug',
                    ])
                    ->orderByDesc('featured')
                    ->orderByDesc('published_at')
                    ->limit(4)
                    ->get(),
                'coverage_countries' => Country::query()
                    ->where('is_covered', true)
                    ->orderBy('sort_order')
                    ->get(['code', 'name_fr']),
                'sponsor' => SponsorSlot::currentlyActive()
                    ->where('placement', 'homepage')
                    ->latest('starts_at')
                    ->first(),
            ];
        });
    }
}
