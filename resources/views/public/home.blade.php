@extends('layouts.public')

@section('title', "Plateforme de l'engagement — L'engagement qui a du sens")
@push('styles')<link href="{{ asset('css/portail.css') }}" rel="stylesheet">@endpush

@section('content')
<section class="hero" aria-labelledby="hero-title">
    <div class="container">
        <div class="row align-items-center g-4">
            <div class="col-lg-7">
                <p class="eyebrow hero-eyebrow">Secteur associatif · humanitaire · philanthropique</p>
                <h1 id="hero-title">L'engagement qui a du sens, réuni au même endroit</h1>
                <p class="hero-lead">ONG, associations, fondations et Waqfs rencontrent les candidats à l'engagement et le mécénat de compétences. Gratuit, transparent, de la France au Maghreb.</p>
                <div class="d-flex flex-column flex-sm-row gap-2">
                    <a href="{{ route('offers.index') }}" class="btn btn-accent btn-lg">Voir les missions</a>
                    <a href="{{ route('sponsorship.create') }}" class="btn btn-outline-light btn-lg">Proposer un mécénat</a>
                </div>
                <p class="hero-meta"><i class="bi bi-geo-alt"></i> {{ $coverage_countries->pluck('name_fr')->join(' · ') }}</p>
            </div>
            <div class="col-lg-5">
                <div class="hero-stats card">
                    <div class="hero-stat"><span class="hero-stat-value">{{ number_format($stats['open_offers'], 0, ',', ' ') }}</span><span class="hero-stat-label">missions ouvertes</span></div>
                    <div class="hero-stat"><span class="hero-stat-value">{{ number_format($stats['verified_organizations'], 0, ',', ' ') }}</span><span class="hero-stat-label">organisations vérifiées</span></div>
                    <div class="hero-stat"><span class="hero-stat-value">{{ $stats['candidate_price'] }}</span><span class="hero-stat-label">gratuit pour les candidats</span></div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="app-section">
    <div class="container">
        <div class="section-head d-flex flex-wrap justify-content-between align-items-end gap-2">
            <div><p class="eyebrow">À la une</p><h2>Missions proposées sur la plateforme</h2><p>Un aperçu des besoins récents.</p></div>
            <a href="{{ route('offers.index') }}" class="btn btn-primary">Voir toutes les missions</a>
        </div>
        <div class="row g-3">
            @forelse ($featured_offers as $offer)
                <div class="col-md-6 col-lg-3">
                    <article class="card offer-card p-3 h-100">
                        <p class="offer-org"><i class="bi bi-building"></i> {{ $offer->organization->name }}</p>
                        <h3>{{ $offer->title }}</h3>
                        <div class="offer-meta">
                            <span><i class="bi bi-geo-alt"></i> {{ $offer->location_label }}</span>
                            <span><i class="bi bi-clock"></i> {{ $offer->duration_label ?: 'Durée à convenir' }}</span>
                        </div>
                        <span class="trust-badge mb-3"><i class="bi bi-patch-check-fill"></i> {{ $offer->organization->verification_label }}</span>
                        <a href="{{ route('offers.show', $offer) }}" class="btn btn-primary btn-sm">Voir la mission</a>
                    </article>
                </div>
            @empty
                <div class="col-12"><div class="alert alert-info">Aucune mission publiée pour le moment.</div></div>
            @endforelse
        </div>
    </div>
</section>

<section class="app-section section-tinted">
    <div class="container">
        <div class="section-head text-center"><h2>Une plateforme pour trois besoins</h2></div>
        <div class="row g-3">
            <div class="col-md-4"><div class="card value-card p-4 h-100"><span class="value-icon"><i class="bi bi-building-check"></i></span><h3>Organisations</h3><p class="text-soft">Publication, ATS, vivier de talents et mécénat.</p><a href="{{ route('login') }}" class="btn btn-outline-primary btn-sm">Espace organisation</a></div></div>
            <div class="col-md-4"><div class="card value-card p-4 h-100"><span class="value-icon"><i class="bi bi-person-badge"></i></span><h3>Candidats</h3><p class="text-soft">Recherche, candidatures et suivi en temps réel.</p><a href="{{ route('login') }}" class="btn btn-outline-primary btn-sm">Espace candidat</a></div></div>
            <div class="col-md-4"><div class="card value-card p-4 h-100"><span class="value-icon"><i class="bi bi-gift"></i></span><h3>Entreprises mécènes</h3><p class="text-soft">Un tunnel léger pour déposer et suivre une mission.</p><a href="{{ route('sponsorship.create') }}" class="btn btn-outline-primary btn-sm">Découvrir le mécénat</a></div></div>
        </div>
    </div>
</section>

<section class="app-section">
    <div class="container">
        <div class="row g-3">
            <div class="col-lg-8"><div class="callout callout-accent h-100"><h3 class="h5">Soutenir la plateforme</h3><p class="text-soft mb-0">Le service reste gratuit pour tous.</p></div></div>
            <div class="col-lg-4">
                <div class="ad-slot h-100">
                    <span class="ad-tag">{{ $sponsor?->label ?? 'Partenariat' }}</span>
                    <p class="mb-0 mt-1">{{ $sponsor?->copy ?? 'Emplacement réservé aux annonceurs alignés, hors zones critiques.' }}</p>
                </div>
            </div>
        </div>
    </div>
</section>
@endsection
