@extends('layouts.public')

@section('title', 'Mécénat de compétences')
@push('styles')<link href="{{ asset('css/mecenat.css') }}" rel="stylesheet">@endpush

@section('content')
<section class="mecenat-hero">
    <div class="container">
        <p class="eyebrow">Entreprises mécènes</p>
        <h1>Vous souhaitez contribuer à l'impact ?</h1>
        <p class="lead">Déposez une mission de mécénat de compétences sans créer un espace entreprise complexe.</p>
        <a href="#depot" class="btn btn-accent btn-lg">Déposer une mission</a>
    </div>
</section>

<section class="app-section section-tinted">
    <div class="container">
        <div class="row g-3 text-center">
            <div class="col-md-4"><div class="card p-4 h-100"><i class="bi bi-pencil-square fs-2"></i><h2 class="h5 mt-2">1. Décrivez</h2><p class="text-soft">Objectifs, livrables, profils et durée.</p></div></div>
            <div class="col-md-4"><div class="card p-4 h-100"><i class="bi bi-bullseye fs-2"></i><h2 class="h5 mt-2">2. Ciblez</h2><p class="text-soft">Mission ouverte, ciblée ou confidentielle.</p></div></div>
            <div class="col-md-4"><div class="card p-4 h-100"><i class="bi bi-file-earmark-check fs-2"></i><h2 class="h5 mt-2">3. Suivez</h2><p class="text-soft">Convention, feuille de temps et reporting.</p></div></div>
        </div>
    </div>
</section>

<section class="app-section" id="depot">
    <div class="container">
        <div class="row justify-content-center"><div class="col-lg-9">
            <div class="card p-4">
                <div class="section-head"><h2>Déposer une mission</h2><p>Les champs marqués * sont obligatoires.</p></div>
                @if($errors->any())<div class="alert alert-danger"><ul class="mb-0">@foreach($errors->all() as $error)<li>{{ $error }}</li>@endforeach</ul></div>@endif
                <form action="{{ route('sponsorship.store') }}" method="post">
                    @csrf
                    <input type="text" name="website" value="" tabindex="-1" autocomplete="off" class="visually-hidden">
                    <div class="row g-3">
                        <div class="col-md-6"><label class="form-label" for="contact_email">E-mail professionnel *</label><input type="email" id="contact_email" name="contact_email" class="form-control" required value="{{ old('contact_email') }}"></div>
                        <div class="col-md-6"><label class="form-label" for="company_name">Raison sociale *</label><input type="text" id="company_name" name="company_name" class="form-control" required value="{{ old('company_name') }}"></div>
                        <div class="col-md-6"><label class="form-label" for="company_legal_id">Identifiant légal</label><input type="text" id="company_legal_id" name="company_legal_id" class="form-control" value="{{ old('company_legal_id') }}"></div>
                        <div class="col-md-6"><label class="form-label" for="country_code">Pays</label><select id="country_code" name="country_code" class="form-select"><option value="">Sélectionner</option>@foreach($countries as $country)<option value="{{ $country->code }}" @selected(old('country_code')===$country->code)>{{ $country->name_fr }}</option>@endforeach</select></div>
                        <div class="col-12"><label class="form-label" for="title">Titre de la mission *</label><input type="text" id="title" name="title" class="form-control" required value="{{ old('title') }}"></div>
                        <div class="col-12"><label class="form-label" for="description">Description</label><textarea id="description" name="description" class="form-control" rows="4">{{ old('description') }}</textarea></div>
                        <div class="col-md-6"><label class="form-label" for="man_days">Nombre de jours-homme *</label><input type="number" id="man_days" name="man_days" class="form-control" min="1" required value="{{ old('man_days') }}"></div>
                        <div class="col-md-6"><label class="form-label" for="visibility">Visibilité *</label><select id="visibility" name="visibility" class="form-select"><option value="open">Libre</option><option value="verified_organizations">ONG vérifiées</option><option value="confidential">Confidentielle</option></select></div>
                        <div class="col-12"><label class="form-label">Causes</label><div class="row">@foreach($causes as $cause)<div class="col-md-4"><div class="form-check"><input class="form-check-input" type="checkbox" name="cause_ids[]" value="{{ $cause->id }}" id="cause-{{ $cause->id }}"><label class="form-check-label" for="cause-{{ $cause->id }}">{{ $cause->name }}</label></div></div>@endforeach</div></div>
                        <div class="col-12"><div class="form-check"><input class="form-check-input" type="checkbox" name="consent" value="1" id="consent" required><label class="form-check-label" for="consent">Je confirme être autorisé à déposer cette mission.</label></div></div>
                    </div>
                    <div class="mt-4 d-flex gap-2"><button type="submit" class="btn btn-accent">Déposer la mission</button><a href="{{ route('home') }}" class="btn btn-subtle">Annuler</a></div>
                </form>
            </div>
        </div></div>
    </div>
</section>
@endsection
