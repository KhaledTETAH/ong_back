<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserRole
{
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        $user = $request->user();

        abort_unless($user, 401, 'Authentification requise.');

        $role = $user->role instanceof \BackedEnum ? $user->role->value : (string) $user->role;

        abort_unless(in_array($role, $roles, true), 403, 'Vous ne disposez pas des permissions nécessaires.');

        return $next($request);
    }
}
