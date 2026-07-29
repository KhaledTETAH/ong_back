<?php

namespace App\Models;

use App\Enums\EngagementType;
use App\Enums\OfferStatus;
use App\Enums\RemoteMode;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Offer extends Model
{
    use SoftDeletes;
    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    protected $fillable = [
        'organization_id',
        'uuid',
        'slug',
        'title',
        'engagement_type',
        'employment_contract',
        'country_code',
        'region',
        'city',
        'address',
        'latitude',
        'longitude',
        'remote_mode',
        'description',
        'responsibilities',
        'desired_profile',
        'conditions',
        'duration_label',
        'duration_days',
        'start_date',
        'end_date',
        'experience_level',
        'status',
        'published_at',
        'expires_at',
        'contact_email',
        'featured',
        'views_count',
    ];

    protected function casts(): array
    {
        return [
            'engagement_type' => EngagementType::class,
            'remote_mode' => RemoteMode::class,
            'status' => OfferStatus::class,
            'latitude' => 'decimal:7',
            'longitude' => 'decimal:7',
            'start_date' => 'date',
            'end_date' => 'date',
            'published_at' => 'datetime',
            'expires_at' => 'datetime',
            'featured' => 'boolean',
        ];
    }

    protected $appends = ['engagement_type_label', 'remote_mode_label', 'location_label'];

    public function getEngagementTypeLabelAttribute(): string
    {
        return $this->engagement_type->label();
    }

    public function getRemoteModeLabelAttribute(): string
    {
        return $this->remote_mode->label();
    }

    public function getLocationLabelAttribute(): string
    {
        $country = $this->relationLoaded('country')
            ? $this->country?->name_fr
            : $this->country_code;

        return collect([$this->city, $country])->filter()->join(', ');
    }

    public function organization(): BelongsTo
    {
        return $this->belongsTo(Organization::class);
    }

    public function country(): BelongsTo
    {
        return $this->belongsTo(Country::class, 'country_code', 'code');
    }

    public function causes(): BelongsToMany
    {
        return $this->belongsToMany(Cause::class);
    }

    public function languages(): BelongsToMany
    {
        return $this->belongsToMany(Language::class);
    }

    public function skills(): BelongsToMany
    {
        return $this->belongsToMany(Skill::class)->withPivot('is_required');
    }

    public function applications(): HasMany
    {
        return $this->hasMany(Application::class);
    }

    public function savedBy(): HasMany
    {
        return $this->hasMany(SavedOffer::class);
    }

    public function events(): HasMany
    {
        return $this->hasMany(OfferEvent::class);
    }

    public function scopePublished(Builder $query): Builder
    {
        return $query
            ->where('status', OfferStatus::Published->value)
            ->whereNotNull('published_at')
            ->where(fn (Builder $q) => $q->whereNull('expires_at')->orWhere('expires_at', '>', now()));
    }
}
