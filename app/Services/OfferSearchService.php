<?php

namespace App\Services;

use App\Enums\OfferStatus;
use App\Models\Offer;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Facades\DB;

class OfferSearchService
{
    public function search(array $filters): LengthAwarePaginator
    {
        $query = Offer::query()
            ->published()
            ->with([
                'organization:id,name,slug,type,country_code,city,description,verification_status,logo_path',
                'organization.country:code,name_fr',
                'country:code,name_fr',
                'causes:id,name,slug',
                'languages:id,code,name_fr',
                'skills:id,name,slug',
            ]);

        $this->applyKeyword($query, $filters['q'] ?? null);
        $this->applyLocation($query, $filters);
        $this->applyStructuredFilters($query, $filters);
        $this->applySorting($query, $filters);

        return $query
            ->paginate((int) ($filters['per_page'] ?? 12))
            ->withQueryString();
    }

    private function applyKeyword(Builder $query, ?string $keyword): void
    {
        if (! $keyword) {
            return;
        }

        $term = '%'.str_replace(['%', '_'], ['\%', '\_'], trim($keyword)).'%';

        $query->where(function (Builder $q) use ($term): void {
            $q->where('offers.title', 'like', $term)
                ->orWhere('offers.description', 'like', $term)
                ->orWhere('offers.desired_profile', 'like', $term)
                ->orWhere('offers.responsibilities', 'like', $term)
                ->orWhereHas('organization', fn (Builder $org) => $org->where('name', 'like', $term))
                ->orWhereHas('causes', fn (Builder $cause) => $cause->where('name', 'like', $term))
                ->orWhereHas('skills', fn (Builder $skill) => $skill->where('name', 'like', $term));
        });
    }

    private function applyLocation(Builder $query, array $filters): void
    {
        if (! empty($filters['country'])) {
            $query->where('offers.country_code', strtoupper($filters['country']));
        }

        if (! empty($filters['city'])) {
            $query->where('offers.city', 'like', '%'.$filters['city'].'%');
        }

        if (! empty($filters['location'])) {
            $location = '%'.trim($filters['location']).'%';
            $query->where(function (Builder $q) use ($location): void {
                $q->where('offers.city', 'like', $location)
                    ->orWhere('offers.region', 'like', $location)
                    ->orWhereHas('country', fn (Builder $country) => $country->where('name_fr', 'like', $location));
            });
        }

        if (
            isset($filters['lat'], $filters['lng']) &&
            DB::connection()->getDriverName() === 'mysql'
        ) {
            $lat = (float) $filters['lat'];
            $lng = (float) $filters['lng'];

            $query->select('offers.*')->selectRaw(
                '(6371 * acos(cos(radians(?)) * cos(radians(latitude)) * cos(radians(longitude) - radians(?)) + sin(radians(?)) * sin(radians(latitude)))) AS distance_km',
                [$lat, $lng, $lat]
            );

            if (! empty($filters['radius_km'])) {
                $query->having('distance_km', '<=', (int) $filters['radius_km']);
            }
        }
    }

    private function applyStructuredFilters(Builder $query, array $filters): void
    {
        if (! empty($filters['type'])) {
            $query->where('offers.engagement_type', $filters['type']);
        }

        if (! empty($filters['cause'])) {
            $query->whereHas('causes', fn (Builder $cause) => $cause->where('slug', $filters['cause']));
        }

        if (! empty($filters['mode'])) {
            $query->whereIn('offers.remote_mode', (array) $filters['mode']);
        }

        if (! empty($filters['language'])) {
            $query->whereHas('languages', fn (Builder $language) => $language->where('code', $filters['language']));
        }

        if (! empty($filters['experience_level'])) {
            $query->where('offers.experience_level', $filters['experience_level']);
        }

        match ($filters['duration'] ?? null) {
            'short' => $query->where('offers.duration_days', '<=', 30),
            'medium' => $query->whereBetween('offers.duration_days', [31, 180]),
            'long' => $query->where(fn (Builder $q) => $q->where('offers.duration_days', '>', 180)->orWhereNull('offers.duration_days')),
            default => null,
        };
    }

    private function applySorting(Builder $query, array $filters): void
    {
        $sort = $filters['sort'] ?? 'relevance';
        $keyword = trim((string) ($filters['q'] ?? ''));

        if ($sort === 'proximity' && isset($filters['lat'], $filters['lng']) && DB::connection()->getDriverName() === 'mysql') {
            $query->orderBy('distance_km')->orderByDesc('published_at');
            return;
        }

        if ($sort === 'oldest') {
            $query->orderBy('published_at');
            return;
        }

        if ($sort === 'recent' || $keyword === '') {
            $query->orderByDesc('featured')->orderByDesc('published_at');
            return;
        }

        $like = '%'.$keyword.'%';
        $prefix = $keyword.'%';

        $query->orderByRaw(
            'CASE
                WHEN offers.title LIKE ? THEN 0
                WHEN offers.title LIKE ? THEN 1
                WHEN offers.description LIKE ? THEN 2
                ELSE 3
             END',
            [$prefix, $like, $like]
        )->orderByDesc('offers.featured')->orderByDesc('offers.published_at');
    }
}
