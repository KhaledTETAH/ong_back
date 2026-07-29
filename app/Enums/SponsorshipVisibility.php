<?php

namespace App\Enums;

enum SponsorshipVisibility: string
{
    case Open = 'open';
    case VerifiedOrganizations = 'verified_organizations';
    case Confidential = 'confidential';
}
