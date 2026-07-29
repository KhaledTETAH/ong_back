<?php

namespace App\Enums;

enum RemoteMode: string
{
    case OnSite = 'on_site';
    case Hybrid = 'hybrid';
    case Remote = 'remote';

    public function label(): string
    {
        return match ($this) {
            self::OnSite => 'Présentiel',
            self::Hybrid => 'Hybride',
            self::Remote => 'À distance',
        };
    }
}
