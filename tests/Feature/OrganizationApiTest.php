<?php

use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->seed();
});

test('directory filters organizations by country and cause', function () {
    $this->getJson('/api/v1/organizations?country=DZ&cause=education')
        ->assertOk()
        ->assertJsonCount(1, 'data')
        ->assertJsonPath('data.0.name', "Association Lumière d'Oran");
});

test('organization detail exposes open offers', function () {
    $this->getJson('/api/v1/organizations/association-lumiere-doran')
        ->assertOk()
        ->assertJsonPath('data.verification.status', 'verified')
        ->assertJsonStructure(['data' => ['offers', 'causes', 'location']]);
});
