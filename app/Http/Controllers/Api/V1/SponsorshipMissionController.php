<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreSponsorshipMissionRequest;
use App\Http\Resources\SponsorshipMissionResource;
use App\Models\SponsorshipMission;
use App\Services\SponsorshipMissionService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class SponsorshipMissionController extends Controller
{
    public function store(
        StoreSponsorshipMissionRequest $request,
        SponsorshipMissionService $service
    ): JsonResponse {
        $result = $service->create($request->validated(), $request);

        return response()->json([
            'message' => 'Mission créée. Confirmez l’adresse e-mail du référent.',
            'data' => new SponsorshipMissionResource($result['mission']),
            'debug_verification_token' => $result['verification_token'],
        ], 201);
    }

    public function show(Request $request, string $trackingUuid): SponsorshipMissionResource
    {
        $mission = SponsorshipMission::where('tracking_uuid', $trackingUuid)->firstOrFail();

        abort_unless(
            hash_equals(
                hash('sha256', (string) $request->query('token')),
                $mission->verification_token_hash
            ),
            403,
            'Jeton de suivi invalide.'
        );

        return new SponsorshipMissionResource($mission->load('causes'));
    }

    public function verify(
        Request $request,
        string $trackingUuid,
        SponsorshipMissionService $service
    ): SponsorshipMissionResource {
        return new SponsorshipMissionResource(
            $service->verify($trackingUuid, (string) $request->input('token'))->load('causes')
        );
    }
}
