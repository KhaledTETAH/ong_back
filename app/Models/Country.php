<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Country extends Model
{
    public $timestamps = false;

    protected $primaryKey = 'code';
    public $incrementing = false;
    protected $keyType = 'string';

    protected $fillable = ['code', 'name_fr', 'is_covered', 'sort_order'];

    protected function casts(): array
    {
        return ['is_covered' => 'boolean'];
    }

    public function organizations(): HasMany
    {
        return $this->hasMany(Organization::class, 'country_code', 'code');
    }
}
