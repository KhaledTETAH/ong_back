<?php

use App\Models\Offer;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->seed();
});

test('offers can be searched by keyword and filtered by country', function () {
    $response = $this->getJson('/api/v1/offers?q=Laravel&country=DZ');

    $response
        ->assertOk()
        ->assertJsonCount(1, 'data')
        ->assertJsonPath('data.0.title', 'Développeur Laravel bénévole');
});

test('offer detail includes organization causes languages and skills', function () {
    $offer = Offer::where('title', 'Coordinateur éducation')->firstOrFail();

    $this->getJson("/api/v1/offers/{$offer->slug}")
        ->assertOk()
        ->assertJsonPath('data.title', 'Coordinateur éducation')
        ->assertJsonPath('data.organization.name', "Association Lumière d'Oran")
        ->assertJsonStructure([
            'data' => ['causes', 'languages', 'skills', 'description', 'desired_profile'],
        ]);
});

test('candidate can save and apply to a published offer only once', function () {
    $candidate = User::whereEmail('candidat@example.test')->firstOrFail();
    $offer = Offer::firstOrFail();

    Sanctum::actingAs($candidate, ['candidate:write']);

    $this->putJson("/api/v1/offers/{$offer->slug}/saved")
        ->assertOk();

    $this->postJson("/api/v1/offers/{$offer->slug}/applications", [
        'cover_letter' => 'Je souhaite contribuer à cette mission.',
    ])->assertCreated();

    $this->postJson("/api/v1/offers/{$offer->slug}/applications", [
        'cover_letter' => 'Deuxième tentative.',
    ])->assertOk();
});
