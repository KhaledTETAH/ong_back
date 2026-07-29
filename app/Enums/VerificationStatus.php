<?php

namespace App\Enums;

enum VerificationStatus: string
{
    case Pending = 'pending';
    case Verified = 'verified';
    case CertifiedPlus = 'certified_plus';
    case Rejected = 'rejected';

    public function label(): string
    {
        return match ($this) {
            self::Pending => 'En cours',
            self::Verified => 'Organisation vérifiée',
            self::CertifiedPlus => 'Certifiée+',
            self::Rejected => 'Non vérifiée',
        };
    }
}
