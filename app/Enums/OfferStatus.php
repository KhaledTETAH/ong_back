<?php

namespace App\Enums;

enum OfferStatus: string
{
    case Draft = 'draft';
    case PendingReview = 'pending_review';
    case Published = 'published';
    case Paused = 'paused';
    case Closed = 'closed';
    case Archived = 'archived';
}
