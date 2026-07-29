<?php

use App\Http\Controllers\Web\AuthController;
use App\Http\Controllers\Web\CandidateOfferActionController;
use App\Http\Controllers\Web\PasswordController;
use App\Http\Controllers\Web\PublicPageController;
use App\Http\Controllers\Web\SocialAuthController;
use App\Http\Controllers\Web\SponsorshipController;
use Illuminate\Foundation\Auth\EmailVerificationRequest;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/', [PublicPageController::class, 'home'])->name('home');

Route::middleware('guest')->group(function (): void {
    Route::get('/connexion', [AuthController::class, 'create'])->name('login');
    Route::post('/connexion', [AuthController::class, 'store'])->middleware('throttle:login')->name('login.store');

    Route::get('/mot-de-passe-oublie', [PasswordController::class, 'requestForm'])->name('password.request');
    Route::post('/mot-de-passe-oublie', [PasswordController::class, 'sendResetLink'])->middleware('throttle:6,1')->name('password.email');
    Route::get('/reinitialiser-mot-de-passe/{token}', [PasswordController::class, 'resetForm'])->name('password.reset');
    Route::post('/reinitialiser-mot-de-passe', [PasswordController::class, 'reset'])->middleware('throttle:6,1')->name('password.update');

    Route::get('/auth/{provider}/redirect', [SocialAuthController::class, 'redirect'])
        ->whereIn('provider', ['google', 'linkedin-openid'])
        ->name('social.redirect');

    Route::get('/auth/{provider}/callback', [SocialAuthController::class, 'callback'])
        ->whereIn('provider', ['google', 'linkedin-openid'])
        ->name('social.callback');
});

Route::post('/deconnexion', [AuthController::class, 'destroy'])
    ->middleware('auth')
    ->name('logout');

Route::get('/missions', [PublicPageController::class, 'offers'])
    ->middleware('throttle:public-search')
    ->name('offers.index');

Route::get('/missions/{offer:slug}', [PublicPageController::class, 'offer'])
    ->name('offers.show');


Route::middleware(['auth', 'verified', 'role:candidate', 'throttle:candidate-actions'])->group(function (): void {
    Route::post('/missions/{offer:slug}/postuler', [CandidateOfferActionController::class, 'apply'])
        ->name('offers.apply');
    Route::put('/missions/{offer:slug}/favori', [CandidateOfferActionController::class, 'save'])
        ->name('offers.save');
    Route::delete('/missions/{offer:slug}/favori', [CandidateOfferActionController::class, 'unsave'])
        ->name('offers.unsave');
});

Route::get('/annuaire', [PublicPageController::class, 'organizations'])
    ->middleware('throttle:public-search')
    ->name('organizations.index');

Route::get('/organisations/{organization:slug}', [PublicPageController::class, 'organization'])
    ->name('organizations.show');

Route::get('/mecenat', [SponsorshipController::class, 'create'])
    ->name('sponsorship.create');

Route::post('/mecenat', [SponsorshipController::class, 'store'])
    ->middleware('throttle:sponsorship-submission')
    ->name('sponsorship.store');

Route::get('/mecenat/verification/{trackingUuid}', [SponsorshipController::class, 'verify'])
    ->name('sponsorship.verify');

Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect()->route('home')->with('success', 'Adresse e-mail vérifiée.');
})->middleware(['auth', 'signed'])->name('verification.verify');

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('success', 'Un nouveau lien de vérification a été envoyé.');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
