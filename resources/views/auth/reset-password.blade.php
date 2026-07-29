@extends('layouts.auth')

@section('title', 'Réinitialiser le mot de passe')

@section('content')
<main class="auth-main">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <section class="auth-card" id="formulaire">
                    <div class="section-head"><h1 class="h2">Choisir un nouveau mot de passe</h1></div>
                    @if ($errors->any())<div class="alert alert-danger"><ul class="mb-0">@foreach($errors->all() as $error)<li>{{ $error }}</li>@endforeach</ul></div>@endif
                    <form method="post" action="{{ route('password.update') }}">
                        @csrf
                        <input type="hidden" name="token" value="{{ $token }}">
                        <div class="mb-3"><label class="form-label" for="email">Adresse e-mail</label><input class="form-control" id="email" name="email" type="email" required autocomplete="email" value="{{ old('email', $email) }}"></div>
                        <div class="mb-3"><label class="form-label" for="password">Nouveau mot de passe</label><input class="form-control" id="password" name="password" type="password" required autocomplete="new-password"></div>
                        <div class="mb-3"><label class="form-label" for="password_confirmation">Confirmation</label><input class="form-control" id="password_confirmation" name="password_confirmation" type="password" required autocomplete="new-password"></div>
                        <div class="d-grid"><button class="btn btn-primary btn-lg" type="submit">Réinitialiser</button></div>
                    </form>
                </section>
            </div>
        </div>
    </div>
</main>
@endsection
