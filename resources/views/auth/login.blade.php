@extends('layouts.auth')

@section('title', 'Connexion')

@section('content')
<main class="auth-main">
    <div class="auth-grid">
        <aside class="auth-aside" aria-label="Présentation de la plateforme">
            <div class="auth-aside-inner">
                <p class="eyebrow auth-eyebrow">L'engagement qui a du sens</p>
                <h1 class="auth-headline">Retrouvez vos candidatures, vos offres et vos missions.</h1>
                <p class="auth-sub">Le point de rencontre du secteur associatif, humanitaire et philanthropique — de la France au Maghreb. Gratuit pour tous.</p>
                <ul class="auth-points">
                    <li><i class="bi bi-search"></i> Recherche par mot-clé et alertes</li>
                    <li><i class="bi bi-clipboard-check"></i> Suivi de candidature en temps réel</li>
                    <li><i class="bi bi-patch-check"></i> Organisations vérifiées avant publication</li>
                </ul>
            </div>
        </aside>

        <section class="auth-panel" aria-labelledby="login-title">
            <div class="auth-card" id="formulaire">
                <div class="section-head">
                    <h2 id="login-title">Se connecter</h2>
                    <p>Accédez à votre espace candidat ou organisation.</p>
                </div>

                @if (session('status'))<div class="alert alert-success">{{ session('status') }}</div>@endif

                @if ($errors->any())
                    <div class="alert alert-danger">
                        <ul class="mb-0">
                            @foreach ($errors->all() as $error)<li>{{ $error }}</li>@endforeach
                        </ul>
                    </div>
                @endif

                <div class="social-stack">
                    <a href="{{ route('social.redirect', 'google') }}" class="btn btn-social"><i class="bi bi-google"></i> Continuer avec Google</a>
                    <a href="{{ route('social.redirect', 'linkedin-openid') }}" class="btn btn-social"><i class="bi bi-linkedin"></i> Continuer avec LinkedIn</a>
                    <button type="button" class="btn btn-social" disabled title="À activer avec les identifiants Apple"><i class="bi bi-apple"></i> Apple — configuration requise</button>
                </div>

                <div class="auth-divider"><span>ou par e-mail</span></div>

                <form action="{{ route('login.store') }}" method="post" novalidate>
                    @csrf
                    <div class="mb-3">
                        <label for="email" class="form-label">Adresse e-mail <span class="req">*</span></label>
                        <input type="email" id="email" name="email" class="form-control" autocomplete="email"
                               required value="{{ old('email') }}" placeholder="prenom.nom@exemple.com">
                    </div>
                    <div class="mb-2">
                        <div class="d-flex justify-content-between align-items-baseline">
                            <label for="password" class="form-label mb-0">Mot de passe <span class="req">*</span></label>
                            <a class="small" href="{{ route('password.request') }}">Mot de passe oublié ?</a>
                        </div>
                        <input type="password" id="password" name="password" class="form-control mt-1"
                               autocomplete="current-password" required placeholder="Votre mot de passe">
                    </div>
                    <div class="form-check my-3">
                        <input class="form-check-input" type="checkbox" id="remember" name="remember" value="1">
                        <label class="form-check-label" for="remember">Rester connecté sur cet appareil</label>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary btn-lg">Se connecter</button>
                    </div>
                </form>

                <p class="auth-alt">Les inscriptions candidat et organisation sont disponibles via l’API documentée dans <code>docs/API_REFERENCE.md</code>.</p>
            </div>
        </section>
    </div>
</main>
@endsection
