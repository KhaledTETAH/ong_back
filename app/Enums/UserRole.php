<?php

namespace App\Enums;

enum UserRole: string
{
    case Candidate = 'candidate';
    case OrganizationAdmin = 'organization_admin';
    case OrganizationRecruiter = 'organization_recruiter';
    case PlatformAdmin = 'platform_admin';
    case Moderator = 'moderator';

    public function label(): string
    {
        return match ($this) {
            self::Candidate => 'Candidat',
            self::OrganizationAdmin => "Administrateur d'organisation",
            self::OrganizationRecruiter => "Recruteur d'organisation",
            self::PlatformAdmin => 'Administrateur plateforme',
            self::Moderator => 'Modérateur',
        };
    }
}
