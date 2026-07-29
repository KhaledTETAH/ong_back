<?php

namespace App\Http\Controllers\Web;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreSponsorshipMissionRequest;
use App\Models\Cause;
use App\Models\Country;
use App\Services\SponsorshipMissionService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class SponsorshipController extends Controller
{
    public function create(): View
    {
        return view('public.sponsorship.create', [
            'causes' => Cause::where('is_active', true)->orderBy('sort_order')->get(),
            'countries' => Country::where('is_covered', true)->orderBy('sort_order')->get(),
        ]);
    }

    public function store(
        StoreSponsorshipMissionRequest $request,
        SponsorshipMissionService $service
    ): RedirectResponse {
        $result = $service->create($request->validated(), $request);

        return redirect()
            ->route('sponsorship.create')
            ->with('success', 'Mission enregistrée. Un e-mail de confirmation vient de vous être envoyé.')
            ->with('tracking_uuid', $result['mission']->tracking_uuid);
    }

    public function verify(
        Request $request,
        string $trackingUuid,
        SponsorshipMissionService $service
    ): View {
        $mission = $service->verify($trackingUuid, (string) $request->query('token'));

        return view('public.sponsorship.verified', compact('mission'));
    }
}
