<?php

namespace App\Http\Controllers\Web;

use App\Enums\AccountStatus;
use App\Enums\UserRole;
use App\Http\Controllers\Controller;
use App\Models\SocialAccount;
use App\Models\User;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use Laravel\Socialite\Facades\Socialite;
use Throwable;

class SocialAuthController extends Controller
{
    private const PROVIDERS = ['google', 'linkedin-openid'];

    public function redirect(string $provider): RedirectResponse
    {
        abort_unless(in_array($provider, self::PROVIDERS, true), 404);

        return Socialite::driver($provider)->redirect();
    }

    public function callback(string $provider): RedirectResponse
    {
        abort_unless(in_array($provider, self::PROVIDERS, true), 404);

        try {
            $socialUser = Socialite::driver($provider)->user();
        } catch (Throwable $e) {
            report($e);
            return redirect()->route('login')->withErrors([
                'email' => 'La connexion externe a échoué. Réessayez ou utilisez votre e-mail.',
            ]);
        }

        $user = DB::transaction(function () use ($provider, $socialUser): User {
            $social = SocialAccount::where('provider', $provider)
                ->where('provider_user_id', $socialUser->getId())
                ->first();

            if ($social) {
                return $social->user;
            }

            $email = $socialUser->getEmail();

            abort_unless($email, 422, 'Le fournisseur n’a pas transmis d’adresse e-mail.');

            $user = User::firstOrCreate(
                ['email' => mb_strtolower($email)],
                [
                    'name' => $socialUser->getName() ?: 'Utilisateur',
                    'password' => null,
                    'role' => UserRole::Candidate,
                    'status' => AccountStatus::Active,
                    'email_verified_at' => now(),
                ]
            );

            $user->socialAccounts()->create([
                'provider' => $provider,
                'provider_user_id' => $socialUser->getId(),
                'provider_email' => $email,
                'access_token' => $socialUser->token,
                'refresh_token' => $socialUser->refreshToken,
                'token_expires_at' => isset($socialUser->expiresIn) ? now()->addSeconds($socialUser->expiresIn) : null,
            ]);

            return $user;
        });

        Auth::login($user, true);
        request()->session()->regenerate();

        return redirect()->intended(route('home'));
    }
}
