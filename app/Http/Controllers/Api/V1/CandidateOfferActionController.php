<?php

namespace App\Http\Controllers\Api\V1;

use App\Enums\ApplicationStatus;
use App\Http\Controllers\Controller;
use App\Http\Requests\ShareOfferRequest;
use App\Http\Requests\StoreApplicationRequest;
use App\Models\Application;
use App\Models\Offer;
use App\Models\OfferEvent;
use App\Models\SavedOffer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class CandidateOfferActionController extends Controller
{
    public function apply(StoreApplicationRequest $request, Offer $offer): JsonResponse
    {
        abort_unless($offer->status->value === 'published', 404);

        $application = Application::firstOrCreate(
            [
                'offer_id' => $offer->id,
                'candidate_id' => $request->user()->id,
            ],
            [
                'cover_letter' => $request->input('cover_letter'),
                'cv_path' => $request->file('cv')?->store("candidate-cvs/{$request->user()->id}", 'local'),
                'status' => ApplicationStatus::New,
                'applied_at' => now(),
            ]
        );

        return response()->json([
            'message' => $application->wasRecentlyCreated
                ? 'Candidature transmise.'
                : 'Vous avez déjà candidaté à cette offre.',
            'data' => [
                'id' => $application->id,
                'status' => $application->status->value,
                'applied_at' => $application->applied_at?->toISOString(),
            ],
        ], $application->wasRecentlyCreated ? 201 : 200);
    }

    public function save(Request $request, Offer $offer): JsonResponse
    {
        SavedOffer::firstOrCreate([
            'user_id' => $request->user()->id,
            'offer_id' => $offer->id,
        ]);

        return response()->json(['message' => 'Offre sauvegardée.']);
    }

    public function unsave(Request $request, Offer $offer): JsonResponse
    {
        SavedOffer::where('user_id', $request->user()->id)
            ->where('offer_id', $offer->id)
            ->delete();

        return response()->json(['message' => 'Offre retirée des favoris.']);
    }

    public function share(ShareOfferRequest $request, Offer $offer): JsonResponse
    {
        OfferEvent::create([
            'offer_id' => $offer->id,
            'user_id' => $request->user()?->id,
            'event_type' => 'share',
            'channel' => $request->input('channel'),
            'ip_hash' => hash('sha256', (string) $request->ip()),
            'user_agent_hash' => hash('sha256', (string) $request->userAgent()),
            'created_at' => now(),
        ]);

        return response()->json(['message' => 'Partage enregistré.']);
    }
}
