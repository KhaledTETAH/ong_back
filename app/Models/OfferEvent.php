<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class OfferEvent extends Model
{
    public $timestamps = false;

    protected $fillable = [
        'offer_id',
        'user_id',
        'event_type',
        'channel',
        'ip_hash',
        'user_agent_hash',
        'created_at',
    ];

    protected function casts(): array
    {
        return ['created_at' => 'datetime'];
    }

    public function offer(): BelongsTo
    {
        return $this->belongsTo(Offer::class);
    }
}
