@extends('layouts.auth')

@section('title', 'Vérifier votre adresse e-mail')

@section('content')
<main class="auth-main">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <section class="auth-card" id="formulaire">
                    <div class="section-head">
                        <h1 class="h2">Vérifiez votre adresse e-mail</h1>
                        <p>Cette vérification est obligatoire avant de postuler ou de sauvegarder une mission.</p>
                    </div>
                    @if (session('success'))<div class="alert alert-success">{{ session('success') }}</div>@endif
                    <form method="post" action="{{ route('verification.send') }}">
                        @csrf
                        <button class="btn btn-primary" type="submit">Renvoyer le lien de vérification</button>
                    </form>
                    <form method="post" action="{{ route('logout') }}" class="mt-3">
                        @csrf
                        <button class="btn btn-subtle" type="submit">Se déconnecter</button>
                    </form>
                </section>
            </div>
        </div>
    </div>
</main>
@endsection
