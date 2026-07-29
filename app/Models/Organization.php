<?php

namespace App\Models;

use App\Enums\VerificationStatus;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Facades\Storage;

class Organization extends Model
{
    use SoftDeletes;
    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    protected $fillable = [
        'owner_user_id',
        'name',
        'slug',
        'type',
        'country_code',
        'city',
        'address',
        'latitude',
        'longitude',
        'registry_number',
        'size',
        'description',
        'mission',
        'verification_status',
        'verified_at',
        'logo_path',
        'website',
        'founded_year',
        'volunteer_count',
        'is_active',
    ];

    protected function casts(): array
    {
        return [
            'verification_status' => VerificationStatus::class,
            'verified_at' => 'datetime',
            'latitude' => 'decimal:7',
            'longitude' => 'decimal:7',
            'is_active' => 'boolean',
        ];
    }

    protected $appends = ['logo_url', 'verification_label'];

    public function getLogoUrlAttribute(): ?string
    {
        return $this->logo_path ? Storage::disk('public')->url($this->logo_path) : null;
    }

    public function getVerificationLabelAttribute(): string
    {
        return $this->verification_status->label();
    }

    public function owner(): BelongsTo
    {
        return $this->belongsTo(User::class, 'owner_user_id');
    }

    public function country(): BelongsTo
    {
        return $this->belongsTo(Country::class, 'country_code', 'code');
    }

    public function causes(): BelongsToMany
    {
        return $this->belongsToMany(Cause::class);
    }

    public function offers(): HasMany
    {
        return $this->hasMany(Offer::class);
    }

    public function documents(): HasMany
    {
        return $this->hasMany(OrganizationDocument::class);
    }

    public function scopePubliclyVisible(Builder $query): Builder
    {
        return $query
            ->where('is_active', true)
            ->whereIn('verification_status', [
                VerificationStatus::Verified->value,
                VerificationStatus::CertifiedPlus->value,
            ]);
    }
}
