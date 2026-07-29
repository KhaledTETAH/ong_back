<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\OfferIndexRequest;
use App\Http\Resources\OfferResource;
use App\Http\Resources\OfferSummaryResource;
use App\Models\Offer;
use App\Services\OfferSearchService;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class OfferController extends Controller
{
    public function index(
        OfferIndexRequest $request,
        OfferSearchService $search
    ): AnonymousResourceCollection {
        return OfferSummaryResource::collection(
            $search->search($request->validated())
        );
    }

    public function show(Offer $offer): OfferResource
    {
        abort_unless($offer->status->value === 'published', 404);

        $offer->load([
            'organization.country',
            'organization.causes',
            'country',
            'causes',
            'languages',
            'skills',
        ])->increment('views_count');

        return new OfferResource($offer);
    }

    public function similar(Offer $offer): AnonymousResourceCollection
    {
        $offer->loadMissing('causes');

        $offers = Offer::published()
            ->whereKeyNot($offer->id)
            ->where(function ($query) use ($offer): void {
                $query->where('engagement_type', $offer->engagement_type->value)
                    ->orWhereHas('causes', fn ($cause) => $cause->whereIn('causes.id', $offer->causes->pluck('id')));
            })
            ->with(['organization:id,name,slug,type,country_code,city,description,verification_status,logo_path', 'organization.country:code,name_fr', 'country:code,name_fr', 'causes:id,name,slug'])
            ->latest('published_at')
            ->limit(6)
            ->get();

        return OfferSummaryResource::collection($offers);
    }
}
