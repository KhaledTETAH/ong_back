@extends('layouts.public')

@section('title', 'Annuaire des organisations')
@push('styles')<link href="{{ asset('css/annuaire.css') }}" rel="stylesheet">@endpush

@section('content')
<section class="page-hero">
    <div class="container">
        <p class="eyebrow">Organisations vérifiées</p>
        <h1>Annuaire des ONG, associations, fondations et Waqfs</h1>
        <form class="search-bar" action="{{ route('organizations.index') }}" method="get">
            <div class="row g-2">
                <div class="col-lg-4"><label class="form-label" for="q">Recherche</label><input id="q" name="q" class="form-control" value="{{ request('q') }}" placeholder="Nom, cause, ville…"></div>
                <div class="col-lg-3"><label class="form-label" for="country">Pays</label><select id="country" name="country" class="form-select"><option value="">Tous</option>@foreach($countries as $country)<option value="{{ $country->code }}" @selected(request('country')===$country->code)>{{ $country->name_fr }}</option>@endforeach</select></div>
                <div class="col-lg-3"><label class="form-label" for="cause">Cause</label><select id="cause" name="cause" class="form-select"><option value="">Toutes</option>@foreach($causes as $cause)<option value="{{ $cause->slug }}" @selected(request('cause')===$cause->slug)>{{ $cause->name }}</option>@endforeach</select></div>
                <div class="col-lg-2 d-flex align-items-end"><button class="btn btn-primary w-100">Rechercher</button></div>
            </div>
        </form>
    </div>
</section>

<section class="app-section" id="resultats">
    <div class="container">
        <div class="row g-4">
            <aside class="col-lg-3">
                <form class="filters card p-3">
                    <input type="hidden" name="q" value="{{ request('q') }}"><input type="hidden" name="country" value="{{ request('country') }}"><input type="hidden" name="cause" value="{{ request('cause') }}">
                    <div class="d-flex justify-content-between"><h2 class="h5">Filtres</h2><a href="{{ route('organizations.index') }}" class="small">Réinitialiser</a></div>
                    <label class="form-label mt-3">Vérification</label>
                    <div class="form-check"><input class="form-check-input" type="checkbox" name="verification[]" value="verified" id="verified" @checked(in_array('verified',(array)request('verification',[]),true))><label class="form-check-label" for="verified">Vérifiée</label></div>
                    <div class="form-check"><input class="form-check-input" type="checkbox" name="verification[]" value="certified_plus" id="certified" @checked(in_array('certified_plus',(array)request('verification',[]),true))><label class="form-check-label" for="certified">Certifiée+</label></div>
                    <label class="form-label mt-3" for="type">Type</label>
                    <select id="type" name="type" class="form-select"><option value="">Tous</option><option value="association">Association</option><option value="foundation">Fondation</option><option value="ngo">ONG</option><option value="waqf">Waqf</option></select>
                    <label class="form-label mt-3" for="size">Taille</label>
                    <select id="size" name="size" class="form-select"><option value="">Toutes</option><option value="micro">1–10</option><option value="small">11–50</option><option value="medium">51–250</option><option value="large">250+</option></select>
                    <button class="btn btn-primary w-100 mt-3">Appliquer</button>
                </form>
            </aside>
            <div class="col-lg-9">
                <div class="d-grid gap-3">
                    @forelse($organizations as $organization)
                        <article class="card p-3">
                            <div class="d-flex flex-wrap justify-content-between gap-3">
                                <div>
                                    <div class="d-flex align-items-center gap-2"><div class="org-logo"><i class="bi bi-building"></i></div><div><h2 class="h4 mb-0">{{ $organization->name }}</h2><span class="trust-badge"><i class="bi bi-patch-check-fill"></i> {{ $organization->verification_label }}</span></div></div>
                                    <p class="text-soft mt-2 mb-2">{{ \Illuminate\Support\Str::limit($organization->description, 180) }}</p>
                                    <div class="offer-meta"><span><i class="bi bi-geo-alt"></i> {{ $organization->city }}, {{ $organization->country->name_fr }}</span><span>{{ $organization->offers_count }} offre(s)</span></div>
                                    <div class="mt-2">@foreach($organization->causes as $cause)<span class="tag">{{ $cause->name }}</span>@endforeach</div>
                                </div>
                                <div class="d-flex align-items-end"><a href="{{ route('organizations.show', $organization) }}" class="btn btn-outline-primary btn-sm">Voir le profil</a></div>
                            </div>
                        </article>
                    @empty
                        <div class="alert alert-info">Aucune organisation trouvée.</div>
                    @endforelse
                </div>
                <div class="mt-4">{{ $organizations->links() }}</div>
            </div>
        </div>
    </div>
</section>
@endsection
