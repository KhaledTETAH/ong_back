<?php

namespace App\Services;

use App\Models\Organization;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Builder;

class OrganizationSearchService
{
    public function search(array $filters): LengthAwarePaginator
    {
        $query = Organization::query()
            ->publiclyVisible()
            ->with(['country:code,name_fr', 'causes:id,name,slug'])
            ->withCount(['offers' => fn (Builder $offer) => $offer->published()]);

        if (! empty($filters['q'])) {
            $term = '%'.trim($filters['q']).'%';
            $query->where(function (Builder $q) use ($term): void {
                $q->where('name', 'like', $term)
                    ->orWhere('description', 'like', $term)
                    ->orWhere('mission', 'like', $term)
                    ->orWhere('city', 'like', $term)
                    ->orWhereHas('causes', fn (Builder $cause) => $cause->where('name', 'like', $term));
            });
        }

        if (! empty($filters['country'])) {
            $query->where('country_code', strtoupper($filters['country']));
        }

        if (! empty($filters['cause'])) {
            $query->whereHas('causes', fn (Builder $cause) => $cause->where('slug', $filters['cause']));
        }

        if (! empty($filters['verification'])) {
            $query->whereIn('verification_status', (array) $filters['verification']);
        }

        if (! empty($filters['type'])) {
            $query->where('type', $filters['type']);
        }

        if (! empty($filters['size'])) {
            $query->where('size', $filters['size']);
        }

        match ($filters['sort'] ?? 'relevance') {
            'name' => $query->orderBy('name'),
            'offers' => $query->orderByDesc('offers_count')->orderBy('name'),
            default => $query->orderByRaw("CASE verification_status WHEN 'certified_plus' THEN 0 WHEN 'verified' THEN 1 ELSE 2 END")
                ->orderByDesc('offers_count')
                ->orderBy('name'),
        };

        return $query
            ->paginate((int) ($filters['per_page'] ?? 12))
            ->withQueryString();
    }
}
