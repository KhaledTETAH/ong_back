<?php

namespace App\Http\Controllers\Web;

use App\Http\Controllers\Controller;
use App\Http\Requests\OfferIndexRequest;
use App\Http\Requests\OrganizationIndexRequest;
use App\Models\Cause;
use App\Models\Country;
use App\Models\Language;
use App\Models\Application;
use App\Models\Offer;
use App\Models\Organization;
use App\Models\SavedOffer;
use App\Services\HomepageService;
use App\Services\OfferSearchService;
use App\Services\OrganizationSearchService;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PublicPageController extends Controller
{
    public function home(HomepageService $homepage): View
    {
        return view('public.home', $homepage->data());
    }

    public function offers(
        OfferIndexRequest $request,
        OfferSearchService $search
    ): View {
        return view('public.offers.index', [
            'offers' => $search->search($request->validated()),
            'causes' => Cause::where('is_active', true)->orderBy('sort_order')->get(),
            'languages' => Language::where('is_active', true)->orderBy('name_fr')->get(),
            'countries' => Country::where('is_covered', true)->orderBy('sort_order')->get(),
            'filters' => $request->validated(),
        ]);
    }

    public function offer(Request $request, Offer $offer): View
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

        $similar = Offer::published()
            ->whereKeyNot($offer->id)
            ->where(function ($query) use ($offer): void {
                $query->where('engagement_type', $offer->engagement_type->value)
                    ->orWhereHas('causes', fn ($cause) => $cause->whereIn('causes.id', $offer->causes->pluck('id')));
            })
            ->with(['organization:id,name,slug,type,country_code,city,description,verification_status,logo_path', 'organization.country:code,name_fr', 'country:code,name_fr'])
            ->latest('published_at')
            ->limit(3)
            ->get();

        $candidate = $request->user()?->isCandidate() ? $request->user() : null;
        $isSaved = $candidate
            ? SavedOffer::where('user_id', $candidate->id)->where('offer_id', $offer->id)->exists()
            : false;
        $hasApplied = $candidate
            ? Application::where('candidate_id', $candidate->id)->where('offer_id', $offer->id)->exists()
            : false;

        return view('public.offers.show', compact('offer', 'similar', 'isSaved', 'hasApplied'));
    }

    public function organizations(
        OrganizationIndexRequest $request,
        OrganizationSearchService $search
    ): View {
        return view('public.organizations.index', [
            'organizations' => $search->search($request->validated()),
            'causes' => Cause::where('is_active', true)->orderBy('sort_order')->get(),
            'countries' => Country::where('is_covered', true)->orderBy('sort_order')->get(),
            'filters' => $request->validated(),
        ]);
    }

    public function organization(Organization $organization): View
    {
        abort_unless($organization->is_active, 404);

        $organization->load([
            'country',
            'causes',
            'offers' => fn ($query) => $query->published()->latest('published_at')->limit(10),
        ]);

        return view('public.organizations.show', compact('organization'));
    }
}
