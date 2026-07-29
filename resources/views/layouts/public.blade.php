<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', "Plateforme de l'engagement")</title>
    <meta name="description" content="@yield('description', 'Plateforme de mise en relation des organisations à mission, candidats et entreprises mécènes.')">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <link href="{{ asset('css/style.css') }}" rel="stylesheet">
    @stack('styles')
</head>
<body class="@yield('body_class')">
<a href="#contenu" class="skip-link">Aller au contenu principal</a>

<header class="site-header">
    <div class="container">
        <div class="header-inner">
            <a href="{{ route('home') }}" class="brand" aria-label="Accueil de la Plateforme de l'engagement">
                <span class="brand-mark" aria-hidden="true"><i class="bi bi-people-fill"></i></span>
                Plateforme de l'engagement
            </a>

            <nav class="main-navigation" aria-label="Navigation principale">
                <ul>
                    <li><a href="{{ route('offers.index') }}" @class(['is-active' => request()->routeIs('offers.*')])>Missions</a></li>
                    <li><a href="{{ route('organizations.index') }}" @class(['is-active' => request()->routeIs('organizations.*')])>Annuaire</a></li>
                    <li><a href="{{ route('sponsorship.create') }}" @class(['is-active' => request()->routeIs('sponsorship.*')])>Mécénat</a></li>
                </ul>
            </nav>

            <div class="header-cta">
                @auth
                    <span class="small text-soft me-2">{{ auth()->user()->name }}</span>
                    <form method="POST" action="{{ route('logout') }}" class="d-inline">
                        @csrf
                        <button class="btn btn-subtle btn-sm" type="submit">Se déconnecter</button>
                    </form>
                @else
                    <a href="{{ route('login') }}" class="btn btn-subtle btn-sm btn-header-desktop">Se connecter</a>
                    <a href="{{ route('login') }}" class="btn btn-primary btn-sm btn-header-desktop">Créer un compte</a>
                @endauth
            </div>

            <details class="mobile-nav">
                <summary aria-label="Ouvrir le menu"><i class="bi bi-list"></i> Menu</summary>
                <ul>
                    <li><a href="{{ route('offers.index') }}">Missions</a></li>
                    <li><a href="{{ route('organizations.index') }}">Annuaire</a></li>
                    <li><a href="{{ route('sponsorship.create') }}">Mécénat</a></li>
                    @auth
                        <li>
                            <form method="POST" action="{{ route('logout') }}">
                                @csrf
                                <button type="submit" class="btn btn-link p-0">Se déconnecter</button>
                            </form>
                        </li>
                    @else
                        <li><a href="{{ route('login') }}">Se connecter</a></li>
                    @endauth
                </ul>
            </details>
        </div>
    </div>
</header>

@if (session('success'))
    <div class="container pt-3">
        <div class="alert alert-success mb-0">{{ session('success') }}</div>
    </div>
@endif

<main id="contenu">
    @yield('content')
</main>

<footer class="site-footer">
    <div class="container">
        <div class="row g-4">
            <div class="col-md-5">
                <a href="{{ route('home') }}" class="brand" style="color:#fff">
                    <span class="brand-mark" aria-hidden="true"><i class="bi bi-people-fill"></i></span>
                    Plateforme de l'engagement
                </a>
                <p class="mt-3 mb-0" style="max-width:42ch">
                    Le point de rencontre du secteur associatif, humanitaire et philanthropique — de la France au Maghreb.
                </p>
            </div>
            <div class="col-6 col-md-3">
                <h4>Explorer</h4>
                <ul>
                    <li><a href="{{ route('offers.index') }}">Missions</a></li>
                    <li><a href="{{ route('organizations.index') }}">Annuaire des ONG</a></li>
                    <li><a href="{{ route('sponsorship.create') }}">Mécénat</a></li>
                </ul>
            </div>
            <div class="col-6 col-md-4">
                <h4>Couverture</h4>
                <p class="mb-0">France · Belgique · Suisse · Algérie · Maroc · Tunisie</p>
            </div>
        </div>
    </div>
</footer>
@stack('scripts')
</body>
</html>
