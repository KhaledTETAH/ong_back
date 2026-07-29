<?php

namespace App\Models;

use App\Enums\SponsorshipStatus;
use App\Enums\SponsorshipVisibility;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Notifications\Notifiable;

class SponsorshipMission extends Model
{
    use Notifiable;
    protected $fillable = [
        'tracking_uuid',
        'contact_email',
        'company_name',
        'company_legal_id',
        'country_code',
        'region',
        'title',
        'description',
        'objectives',
        'deliverables',
        'required_profiles',
        'man_days',
        'visibility',
        'status',
        'verification_token_hash',
        'verified_email_at',
        'consent_at',
        'submitted_ip',
        'user_agent',
    ];

    protected $hidden = [
        'verification_token_hash',
        'submitted_ip',
        'user_agent',
    ];

    protected function casts(): array
    {
        return [
            'visibility' => SponsorshipVisibility::class,
            'status' => SponsorshipStatus::class,
            'verified_email_at' => 'datetime',
            'consent_at' => 'datetime',
        ];
    }

    public function routeNotificationForMail(): string
    {
        return $this->contact_email;
    }

    public function causes(): BelongsToMany
    {
        return $this->belongsToMany(Cause::class);
    }
}
