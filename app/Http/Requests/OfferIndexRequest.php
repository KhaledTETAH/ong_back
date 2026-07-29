<?php

namespace App\Http\Requests;

use App\Enums\EngagementType;
use App\Enums\RemoteMode;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class OfferIndexRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'q' => ['nullable', 'string', 'max:150'],
            'location' => ['nullable', 'string', 'max:150'],
            'country' => ['nullable', 'string', 'size:2', 'exists:countries,code'],
            'city' => ['nullable', 'string', 'max:120'],
            'type' => ['nullable', Rule::enum(EngagementType::class)],
            'cause' => ['nullable', 'string', 'exists:causes,slug'],
            'mode' => ['nullable'],
            'mode.*' => [Rule::enum(RemoteMode::class)],
            'duration' => ['nullable', Rule::in(['short', 'medium', 'long'])],
            'language' => ['nullable', 'string', 'exists:languages,code'],
            'experience_level' => ['nullable', Rule::in(['junior', 'confirmed', 'senior', 'expert', 'governance'])],
            'sort' => ['nullable', Rule::in(['relevance', 'recent', 'oldest', 'proximity'])],
            'lat' => ['nullable', 'numeric', 'between:-90,90'],
            'lng' => ['nullable', 'numeric', 'between:-180,180'],
            'radius_km' => ['nullable', 'integer', 'between:1,500'],
            'page' => ['nullable', 'integer', 'min:1'],
            'per_page' => ['nullable', 'integer', 'between:1,50'],
        ];
    }

    protected function prepareForValidation(): void
    {
        $mode = $this->input('mode');

        if (is_string($mode) && str_contains($mode, ',')) {
            $this->merge(['mode' => array_filter(explode(',', $mode))]);
        } elseif (is_string($mode)) {
            $this->merge(['mode' => [$mode]]);
        }
    }
}
