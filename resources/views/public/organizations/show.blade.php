@extends('layouts.public')
@section('title', $organization->name)

@section('content')
<section class="page-hero"><div class="container"><span class="trust-badge">{{ $organization->verification_label }}</span><h1 class="mt-2">{{ $organization->name }}</h1><p>{{ $organization->city }}, {{ $organization->country->name_fr }} · {{ ucfirst($organization->type) }}</p></div></section>
<section class="app-section"><div class="container"><div class="row g-4"><div class="col-lg-8"><div class="card p-4"><h2>À propos</h2><p>{{ $organization->description }}</p>@if($organization->mission)<h3 class="h5">Mission</h3><p>{{ $organization->mission }}</p>@endif<h2 class="mt-4">Offres ouvertes</h2>@forelse($organization->offers as $offer)<div class="border-top py-3"><a href="{{ route('offers.show',$offer) }}"><strong>{{ $offer->title }}</strong></a><div class="text-soft">{{ $offer->location_label }} · {{ $offer->duration_label }}</div></div>@empty<p>Aucune offre ouverte.</p>@endforelse</div></div><aside class="col-lg-4"><div class="card p-4"><h2 class="h5">En un coup d'œil</h2><p>Fondée en {{ $organization->founded_year ?: '—' }}</p><p>{{ number_format($organization->volunteer_count,0,',',' ') }} bénévoles</p><div>@foreach($organization->causes as $cause)<span class="tag">{{ $cause->name }}</span>@endforeach</div></div></aside></div></div></section>
@endsection
