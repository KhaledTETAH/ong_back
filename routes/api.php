<?php

use App\Http\Controllers\Api\V1\AuthController;
use App\Http\Controllers\Api\V1\CandidateOfferActionController;
use App\Http\Controllers\Api\V1\HomeController;
use App\Http\Controllers\Api\V1\OfferController;
use App\Http\Controllers\Api\V1\OrganizationController;
use App\Http\Controllers\Api\V1\PasswordController;
use App\Http\Controllers\Api\V1\RegistrationController;
use App\Http\Controllers\Api\V1\SponsorshipMissionController;
use Illuminate\Support\Facades\Route;

Route::prefix('v1')->group(function (): void {
    Route::get('/home', HomeController::class);

    Route::prefix('auth')->group(function (): void {
        Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:login');
        Route::post('/register/candidate', [RegistrationController::class, 'candidate'])->middleware('throttle:6,1');
        Route::post('/register/organization', [RegistrationController::class, 'organization'])->middleware('throttle:3,1');
        Route::post('/forgot-password', [PasswordController::class, 'forgot'])->middleware('throttle:6,1');
        Route::post('/reset-password', [PasswordController::class, 'reset'])->middleware('throttle:6,1');

        Route::middleware('auth:sanctum')->group(function (): void {
            Route::get('/me', [AuthController::class, 'me']);
            Route::post('/logout', [AuthController::class, 'logout']);
        });
    });

    Route::get('/offers', [OfferController::class, 'index'])->middleware('throttle:public-search');
    Route::get('/offers/{offer:slug}', [OfferController::class, 'show']);
    Route::get('/offers/{offer:slug}/similar', [OfferController::class, 'similar']);
    Route::post('/offers/{offer:slug}/share', [CandidateOfferActionController::class, 'share'])->middleware('throttle:60,1');

    Route::get('/organizations', [OrganizationController::class, 'index'])->middleware('throttle:public-search');
    Route::get('/organizations/{organization:slug}', [OrganizationController::class, 'show']);

    Route::post('/sponsorship-missions', [SponsorshipMissionController::class, 'store'])
        ->middleware('throttle:sponsorship-submission');
    Route::get('/sponsorship-missions/{trackingUuid}', [SponsorshipMissionController::class, 'show']);
    Route::post('/sponsorship-missions/{trackingUuid}/verify', [SponsorshipMissionController::class, 'verify'])
        ->middleware('throttle:10,1');

    Route::middleware(['auth:sanctum', 'verified', 'role:candidate', 'throttle:candidate-actions'])->group(function (): void {
        Route::post('/offers/{offer:slug}/applications', [CandidateOfferActionController::class, 'apply']);
        Route::put('/offers/{offer:slug}/saved', [CandidateOfferActionController::class, 'save']);
        Route::delete('/offers/{offer:slug}/saved', [CandidateOfferActionController::class, 'unsave']);
    });
});
