<?php

namespace App\Enums;

enum ApplicationStatus: string
{
    case New = 'new';
    case PreQualified = 'pre_qualified';
    case Interview = 'interview';
    case Decision = 'decision';
    case Offer = 'offer';
    case Accepted = 'accepted';
    case Rejected = 'rejected';
    case TalentPool = 'talent_pool';
    case Withdrawn = 'withdrawn';
}
