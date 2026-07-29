@extends('layouts.auth')

@section('title', 'Mot de passe oublié')

@section('content')
<main class="auth-main">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <section class="auth-card" id="formulaire">
                    <div class="section-head">
                        <h1 class="h2">Mot de passe oublié</h1>
                        <p>Indiquez votre adresse e-mail. Le message de réponse reste neutre pour protéger les comptes.</p>
                    </div>

                    @if (session('status'))<div class="alert alert-success">{{ session('status') }}</div>@endif
                    @if ($errors->any())<div class="alert alert-danger"><ul class="mb-0">@foreach($errors->all() as $error)<li>{{ $error }}</li>@endforeach</ul></div>@endif

                    <form method="post" action="{{ route('password.email') }}">
                        @csrf
                        <label class="form-label" for="email">Adresse e-mail</label>
                        <input class="form-control" id="email" name="email" type="email" required autocomplete="email" value="{{ old('email') }}">
                        <div class="d-grid mt-3"><button class="btn btn-primary btn-lg" type="submit">Envoyer le lien</button></div>
                    </form>
                    <p class="auth-alt"><a href="{{ route('login') }}">Retour à la connexion</a></p>
                </section>
            </div>
        </div>
    </div>
</main>
@endsection
