<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', 'Connexion') — Plateforme de l'engagement</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <link href="{{ asset('css/style.css') }}" rel="stylesheet">
    <link href="{{ asset('css/login.css') }}" rel="stylesheet">
</head>
<body class="auth-body">
<a href="#formulaire" class="skip-link">Aller au formulaire</a>
<header class="site-header">
    <div class="container">
        <div class="header-inner">
            <a href="{{ route('home') }}" class="brand">
                <span class="brand-mark" aria-hidden="true"><i class="bi bi-people-fill"></i></span>
                Plateforme de l'engagement
            </a>
            <a href="{{ route('home') }}" class="btn btn-subtle btn-sm">
                <i class="bi bi-arrow-left"></i> Retour au portail
            </a>
        </div>
    </div>
</header>
@yield('content')
</body>
</html>
