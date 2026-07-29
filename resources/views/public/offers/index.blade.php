@extends('layouts.public')

@section('title', 'Missions')
@push('styles')<link href="{{ asset('css/missions.css') }}" rel="stylesheet">@endpush

@section('content')
<section class="page-hero">
    <div class="container">
        <p class="eyebrow">Recherche par mot-clé</p>
        <h1>Trouvez une mission qui correspond à vos compétences</h1>
        <form class="search-bar" action="{{ route('offers.index') }}" method="get" role="search">
            <div class="row g-2">
                <div class="col-lg-4"><label for="q" class="form-label">Mot-clé</label><input type="search" id="q" name="q" class="form-control" value="{{ request('q') }}" placeholder="Intitulé, compétence, cause"></div>
                <div class="col-lg-3"><label for="location" class="form-label">Lieu</label><input type="text" id="location" name="location" class="form-control" value="{{ request('location') }}" placeholder="Ville ou pays"></div>
                <div class="col-lg-3"><label for="type" class="form-label">Type</label>
                    <select id="type" name="type" class="form-select">
                        <option value="">Tous les types</option>
                        @foreach (\App\Enums\EngagementType::cases() as $type)
                            <option value="{{ $type->value }}" @selected(request('type') === $type->value)>{{ $type->label() }}</option>
                        @endforeach
                    </select>
                </div>
                <div class="col-lg-2 d-flex align-items-end"><button type="submit" class="btn btn-primary w-100">Rechercher</button></div>
            </div>
        </form>
    </div>
</section>

<section class="app-section" id="resultats">
    <div class="container">
        <div class="row g-4">
            <aside class="col-lg-3">
                <form class="filters card p-3" action="{{ route('offers.index') }}" method="get">
                    <input type="hidden" name="q" value="{{ request('q') }}">
                    <input type="hidden" name="location" value="{{ request('location') }}">
                    <div class="d-flex justify-content-between"><h2 class="h5">Filtres</h2><a href="{{ route('offers.index') }}" class="small">Réinitialiser</a></div>
                    <label class="form-label mt-3" for="cause">Cause</label>
                    <select id="cause" name="cause" class="form-select"><option value="">Toutes</option>@foreach($causes as $cause)<option value="{{ $cause->slug }}" @selected(request('cause')===$cause->slug)>{{ $cause->name }}</option>@endforeach</select>
                    <label class="form-label mt-3">Modalité</label>
                    @foreach (\App\Enums\RemoteMode::cases() as $mode)
                        <div class="form-check"><input class="form-check-input" type="checkbox" name="mode[]" value="{{ $mode->value }}" id="mode-{{ $mode->value }}" @checked(in_array($mode->value, (array) request('mode', []), true))><label class="form-check-label" for="mode-{{ $mode->value }}">{{ $mode->label() }}</label></div>
                    @endforeach
                    <label class="form-label mt-3" for="duration">Durée</label>
                    <select id="duration" name="duration" class="form-select"><option value="">Toutes</option><option value="short" @selected(request('duration')==='short')>Jusqu'à 1 mois</option><option value="medium" @selected(request('duration')==='medium')>1 à 6 mois</option><option value="long" @selected(request('duration')==='long')>Plus de 6 mois</option></select>
                    <label class="form-label mt-3" for="language">Langue</label>
                    <select id="language" name="language" class="form-select"><option value="">Toutes</option>@foreach($languages as $language)<option value="{{ $language->code }}" @selected(request('language')===$language->code)>{{ $language->name_fr }}</option>@endforeach</select>
                    <button type="submit" class="btn btn-primary w-100 mt-3">Appliquer</button>
                </form>
            </aside>

            <div class="col-lg-9">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <p class="mb-0"><strong>{{ $offers->total() }}</strong> résultat(s)</p>
                    <form><input type="hidden" name="q" value="{{ request('q') }}"><select name="sort" class="form-select form-select-sm" onchange="this.form.submit()"><option value="relevance" @selected(request('sort','relevance')==='relevance')>Pertinence</option><option value="recent" @selected(request('sort')==='recent')>Plus récentes</option><option value="oldest" @selected(request('sort')==='oldest')>Plus anciennes</option></select></form>
                </div>

                <div class="d-grid gap-3">
                    @forelse($offers as $offer)
                        <article class="card p-3">
                            <div class="d-flex flex-wrap justify-content-between gap-3">
                                <div>
                                    <p class="offer-org mb-1"><i class="bi bi-building"></i> {{ $offer->organization->name }}</p>
                                    <h2 class="h4 mb-2">{{ $offer->title }}</h2>
                                    <div class="offer-meta"><span><i class="bi bi-geo-alt"></i> {{ $offer->location_label }}</span><span><i class="bi bi-clock"></i> {{ $offer->duration_label ?: 'À convenir' }}</span><span>{{ $offer->remote_mode_label }}</span></div>
                                    <div class="mt-2">@foreach($offer->causes as $cause)<span class="tag">{{ $cause->name }}</span>@endforeach</div>
                                </div>
                                <div class="d-flex flex-column align-items-end justify-content-between">
                                    <span class="trust-badge"><i class="bi bi-patch-check-fill"></i> {{ $offer->organization->verification_label }}</span>
                                    <a href="{{ route('offers.show', $offer) }}" class="btn btn-primary btn-sm">Voir la mission</a>
                                </div>
                            </div>
                        </article>
                    @empty
                        <div class="alert alert-info">Aucune mission ne correspond aux critères.</div>
                    @endforelse
                </div>
                <div class="mt-4">{{ $offers->links() }}</div>
            </div>
        </div>
    </div>
</section>
@endsection
