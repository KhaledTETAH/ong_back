@extends('layouts.public')

@section('title', $offer->title)
@push('styles')<link href="{{ asset('css/offre.css') }}" rel="stylesheet">@endpush

@section('content')
<section class="app-section">
    <div class="container">
        <nav aria-label="Fil d'Ariane"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="{{ route('home') }}">Accueil</a></li><li class="breadcrumb-item"><a href="{{ route('offers.index') }}">Missions</a></li><li class="breadcrumb-item active">{{ $offer->title }}</li></ol></nav>
        <div class="row g-4">
            <div class="col-lg-8">
                <article class="card p-4">
                    <p class="offer-org"><a href="{{ route('organizations.show',$offer->organization) }}">{{ $offer->organization->name }}</a> <span class="trust-badge"><i class="bi bi-patch-check-fill"></i> {{ $offer->organization->verification_label }}</span></p>
                    <h1>{{ $offer->title }}</h1>
                    <div class="offer-meta mb-3"><span><i class="bi bi-geo-alt"></i> {{ $offer->location_label }}</span><span>{{ $offer->engagement_type_label }}</span><span>{{ $offer->remote_mode_label }}</span><span>{{ $offer->duration_label }}</span></div>
                    <div class="mb-3">@foreach($offer->causes as $cause)<span class="tag">{{ $cause->name }}</span>@endforeach</div>
                    <h2 class="h4">Description de la mission</h2><div class="preserve-lines">{{ $offer->description }}</div>
                    @if($offer->responsibilities)<h2 class="h4 mt-4">Responsabilités</h2><div class="preserve-lines">{{ $offer->responsibilities }}</div>@endif
                    @if($offer->desired_profile)<h2 class="h4 mt-4">Profil recherché</h2><div class="preserve-lines">{{ $offer->desired_profile }}</div>@endif
                    @if($offer->conditions)<h2 class="h4 mt-4">Conditions</h2><div class="preserve-lines">{{ $offer->conditions }}</div>@endif
                    <div class="mt-4">
                        @auth
                            @if(auth()->user()->isCandidate())
                                <div class="d-flex flex-wrap gap-2 align-items-center">
                                    @if($hasApplied)
                                        <span class="btn btn-success btn-lg disabled"><i class="bi bi-check-circle"></i> Candidature transmise</span>
                                    @else
                                        <details class="w-100">
                                            <summary class="btn btn-primary btn-lg">Postuler à cette mission</summary>
                                            <form class="card p-3 mt-3" action="{{ route('offers.apply', $offer) }}" method="post" enctype="multipart/form-data">
                                                @csrf
                                                <label class="form-label" for="cover_letter">Message de motivation</label>
                                                <textarea class="form-control" id="cover_letter" name="cover_letter" rows="5" maxlength="10000">{{ old('cover_letter') }}</textarea>
                                                <label class="form-label mt-3" for="cv">CV facultatif (PDF, DOC, DOCX — 5 Mo max.)</label>
                                                <input class="form-control" type="file" id="cv" name="cv" accept=".pdf,.doc,.docx">
                                                <div class="mt-3"><button class="btn btn-primary" type="submit">Envoyer ma candidature</button></div>
                                            </form>
                                        </details>
                                    @endif

                                    @if($isSaved)
                                        <form action="{{ route('offers.unsave', $offer) }}" method="post">
                                            @csrf @method('DELETE')
                                            <button class="btn btn-subtle" type="submit"><i class="bi bi-bookmark-fill"></i> Retirer des favoris</button>
                                        </form>
                                    @else
                                        <form action="{{ route('offers.save', $offer) }}" method="post">
                                            @csrf @method('PUT')
                                            <button class="btn btn-subtle" type="submit"><i class="bi bi-bookmark"></i> Sauvegarder l'offre</button>
                                        </form>
                                    @endif
                                </div>
                            @else
                                <div class="alert alert-info mb-0">La candidature est réservée aux comptes candidats.</div>
                            @endif
                        @else
                            <div class="d-flex flex-wrap gap-2">
                                <a href="{{ route('login') }}" class="btn btn-primary btn-lg">Se connecter pour postuler</a>
                                <a href="{{ route('login') }}" class="btn btn-subtle"><i class="bi bi-bookmark"></i> Sauvegarder l'offre</a>
                            </div>
                        @endauth
                    </div>
                </article>
            </div>
            <aside class="col-lg-4">
                <div class="card p-4 mb-3">
                    <h2 class="h5">{{ $offer->organization->name }}</h2>
                    <p class="text-soft">{{ \Illuminate\Support\Str::limit($offer->organization->description, 180) }}</p>
                    <a href="{{ route('organizations.show',$offer->organization) }}" class="btn btn-outline-primary btn-sm w-100">Voir le profil</a>
                </div>
                <div class="card p-4">
                    <h2 class="h5">Missions similaires</h2>
                    @forelse($similar as $item)
                        <div class="border-top py-3"><a href="{{ route('offers.show',$item) }}"><strong>{{ $item->title }}</strong></a><div class="text-soft small">{{ $item->organization->name }}</div></div>
                    @empty<p class="text-soft mb-0">Aucune mission similaire.</p>@endforelse
                </div>
            </aside>
        </div>
    </div>
</section>
<style>.preserve-lines{white-space:pre-line}</style>
@endsection
