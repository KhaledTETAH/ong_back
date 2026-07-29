<?php

namespace App\Enums;

enum SponsorshipStatus: string
{
    case PendingEmailVerification = 'pending_email_verification';
    case Submitted = 'submitted';
    case UnderReview = 'under_review';
    case Matched = 'matched';
    case InProgress = 'in_progress';
    case Completed = 'completed';
    case Rejected = 'rejected';
}
