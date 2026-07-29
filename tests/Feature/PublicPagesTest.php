<?php

use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->seed();
});

test('the first six dynamic pages render successfully', function () {
    $this->get('/')->assertOk()->assertSee("L'engagement qui a du sens");
    $this->get('/connexion')->assertOk()->assertSee('Se connecter');
    $this->get('/missions')->assertOk()->assertSee('Coordinateur éducation');
    $this->get('/annuaire')->assertOk()->assertSee("Association Lumière d'Oran");
    $this->get('/mecenat')->assertOk()->assertSee('Déposer une mission');
    $this->get('/missions/coordinateur-education-1')->assertOk()->assertSee('Coordinateur éducation');
});

test('authenticated candidate can save and apply from the offer page', function () {
    $candidate = \App\Models\User::whereEmail('candidat@example.test')->firstOrFail();
    $offer = \App\Models\Offer::where('title', 'Coordinateur éducation')->firstOrFail();

    $this->actingAs($candidate)
        ->put("/missions/{$offer->slug}/favori")
        ->assertRedirect();

    $this->actingAs($candidate)
        ->post("/missions/{$offer->slug}/postuler", [
            'cover_letter' => 'Candidature envoyée depuis la page web.',
        ])
        ->assertRedirect();

    $this->assertDatabaseHas('saved_offers', [
        'user_id' => $candidate->id,
        'offer_id' => $offer->id,
    ]);

    $this->assertDatabaseHas('applications', [
        'candidate_id' => $candidate->id,
        'offer_id' => $offer->id,
    ]);
});

test('forgot password form renders and accepts a neutral request', function () {
    \Illuminate\Support\Facades\Notification::fake();

    $this->get('/mot-de-passe-oublie')
        ->assertOk()
        ->assertSee('Mot de passe oublié');

    $this->post('/mot-de-passe-oublie', ['email' => 'candidat@example.test'])
        ->assertRedirect()
        ->assertSessionHas('status');
});
