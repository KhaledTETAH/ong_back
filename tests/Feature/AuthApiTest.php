<?php

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->seed();
});

test('candidate can log in and receive a sanctum token', function () {
    $response = $this->postJson('/api/v1/auth/login', [
        'email' => 'candidat@example.test',
        'password' => 'Password123!',
        'device_name' => 'Pest',
    ]);

    $response
        ->assertOk()
        ->assertJsonPath('data.user.email', 'candidat@example.test')
        ->assertJsonPath('data.token_type', 'Bearer');

    expect($response->json('data.token'))->toBeString()->not->toBeEmpty();
});

test('invalid credentials are rejected', function () {
    $this->postJson('/api/v1/auth/login', [
        'email' => 'candidat@example.test',
        'password' => 'wrong-password',
    ])->assertUnprocessable();
});

test('candidate registration validates and creates a user', function () {
    $this->postJson('/api/v1/auth/register/candidate', [
        'name' => 'Samira Test',
        'email' => 'samira@example.test',
        'password' => 'StrongPassword123!',
        'password_confirmation' => 'StrongPassword123!',
        'locale' => 'fr',
    ])->assertCreated()
      ->assertJsonPath('data.email', 'samira@example.test');

    expect(User::whereEmail('samira@example.test')->exists())->toBeTrue();
});
