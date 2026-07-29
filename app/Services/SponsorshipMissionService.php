<?php

namespace App\Services;

use App\Enums\SponsorshipStatus;
use App\Models\SponsorshipMission;
use App\Notifications\VerifySponsorshipMission;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class SponsorshipMissionService
{
    public function create(array $data, Request $request): array
    {
        return DB::transaction(function () use ($data, $request): array {
            $plainToken = Str::random(64);

            $mission = SponsorshipMission::create([
                ...collect($data)->except(['cause_ids', 'consent', 'website'])->all(),
                'tracking_uuid' => (string) Str::uuid(),
                'status' => SponsorshipStatus::PendingEmailVerification,
                'verification_token_hash' => hash('sha256', $plainToken),
                'consent_at' => now(),
                'submitted_ip' => $request->ip(),
                'user_agent' => mb_substr((string) $request->userAgent(), 0, 1000),
            ]);

            $mission->causes()->sync($data['cause_ids'] ?? []);

            $mission->notify(new VerifySponsorshipMission($plainToken));

            return [
                'mission' => $mission->fresh('causes'),
                'verification_token' => app()->isLocal() || app()->runningUnitTests() ? $plainToken : null,
            ];
        });
    }

    public function verify(string $trackingUuid, string $plainToken): SponsorshipMission
    {
        $mission = SponsorshipMission::where('tracking_uuid', $trackingUuid)->firstOrFail();

        abort_unless(
            hash_equals($mission->verification_token_hash, hash('sha256', $plainToken)),
            403,
            'Lien de vérification invalide.'
        );

        if (! $mission->verified_email_at) {
            $mission->forceFill([
                'verified_email_at' => now(),
                'status' => SponsorshipStatus::Submitted,
            ])->save();
        }

        return $mission;
    }
}
