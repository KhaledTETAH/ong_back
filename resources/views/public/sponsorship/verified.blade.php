@extends('layouts.public')
@section('title', 'Mission confirmée')
@section('content')
<section class="app-section"><div class="container"><div class="row justify-content-center"><div class="col-lg-7"><div class="card p-5 text-center"><i class="bi bi-check-circle-fill text-success fs-1"></i><h1 class="h2 mt-3">Adresse e-mail confirmée</h1><p>La mission « {{ $mission->title }} » est maintenant transmise à l'équipe de modération.</p><p class="text-soft">Référence : {{ $mission->tracking_uuid }}</p><a href="{{ route('home') }}" class="btn btn-primary">Retour au portail</a></div></div></div></div></section>
@endsection
