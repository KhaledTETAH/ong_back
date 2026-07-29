<?php

use App\Models\Cause;
use App\Models\SponsorshipMission;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->seed();
    Notification::fake();
});

test('company representative can submit a sponsorship mission', function () {
    $cause = Cause::where('slug', 'inclusion-numerique')->firstOrFail();

    $response = $this->postJson('/api/v1/sponsorship-missions', [
        'contact_email' => 'mecenat@entreprise.test',
        'company_name' => 'Entreprise Solidaire',
        'company_legal_id' => 'RC-2026-001',
        'country_code' => 'FR',
        'title' => 'Audit de cybersécurité solidaire',
        'description' => 'Audit et plan de remédiation pour une ONG.',
        'man_days' => 12,
        'visibility' => 'verified_organizations',
        'cause_ids' => [$cause->id],
        'consent' => true,
        'website' => '',
    ]);

    $response
        ->assertCreated()
        ->assertJsonPath('data.company_name', 'Entreprise Solidaire')
        ->assertJsonPath('data.status', 'pending_email_verification');

    expect(SponsorshipMission::count())->toBe(1);
});

test('honeypot rejects automated sponsorship submission', function () {
    $this->postJson('/api/v1/sponsorship-missions', [
        'contact_email' => 'bot@example.test',
        'company_name' => 'Bot',
        'title' => 'Spam',
        'man_days' => 1,
        'visibility' => 'open',
        'consent' => true,
        'website' => 'https://spam.invalid',
    ])->assertUnprocessable();
});
