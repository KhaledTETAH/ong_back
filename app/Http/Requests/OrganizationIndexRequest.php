<?php

namespace App\Http\Requests;

use App\Enums\VerificationStatus;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class OrganizationIndexRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'q' => ['nullable', 'string', 'max:150'],
            'country' => ['nullable', 'string', 'size:2', 'exists:countries,code'],
            'cause' => ['nullable', 'string', 'exists:causes,slug'],
            'verification' => ['nullable'],
            'verification.*' => [Rule::enum(VerificationStatus::class)],
            'type' => ['nullable', Rule::in(['association', 'foundation', 'ngo', 'waqf'])],
            'size' => ['nullable', Rule::in(['micro', 'small', 'medium', 'large'])],
            'sort' => ['nullable', Rule::in(['relevance', 'name', 'offers'])],
            'page' => ['nullable', 'integer', 'min:1'],
            'per_page' => ['nullable', 'integer', 'between:1,50'],
        ];
    }

    protected function prepareForValidation(): void
    {
        $verification = $this->input('verification');

        if (is_string($verification) && str_contains($verification, ',')) {
            $this->merge(['verification' => array_filter(explode(',', $verification))]);
        } elseif (is_string($verification)) {
            $this->merge(['verification' => [$verification]]);
        }
    }
}
