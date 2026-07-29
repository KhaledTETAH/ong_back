<?php

namespace App\Http\Controllers\Web;

use App\Enums\ApplicationStatus;
use App\Http\Controllers\Controller;
use App\Http\Requests\StoreApplicationRequest;
use App\Models\Application;
use App\Models\Offer;
use App\Models\SavedOffer;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class CandidateOfferActionController extends Controller
{
    public function apply(StoreApplicationRequest $request, Offer $offer): RedirectResponse
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

        return back()->with(
            'success',
            $application->wasRecentlyCreated
                ? 'Votre candidature a été transmise.'
                : 'Vous avez déjà candidaté à cette mission.'
        );
    }

    public function save(Request $request, Offer $offer): RedirectResponse
    {
        SavedOffer::firstOrCreate([
            'user_id' => $request->user()->id,
            'offer_id' => $offer->id,
        ]);

        return back()->with('success', 'Mission ajoutée à vos favoris.');
    }

    public function unsave(Request $request, Offer $offer): RedirectResponse
    {
        SavedOffer::where('user_id', $request->user()->id)
            ->where('offer_id', $offer->id)
            ->delete();

        return back()->with('success', 'Mission retirée de vos favoris.');
    }
}
