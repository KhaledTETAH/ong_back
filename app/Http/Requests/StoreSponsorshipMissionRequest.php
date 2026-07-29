<?php

namespace App\Http\Requests;

use App\Enums\SponsorshipVisibility;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StoreSponsorshipMissionRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'contact_email' => ['required', 'email:rfc', 'max:255'],
            'company_name' => ['required', 'string', 'max:180'],
            'company_legal_id' => ['nullable', 'string', 'max:120'],
            'country_code' => ['nullable', 'string', 'size:2', 'exists:countries,code'],
            'region' => ['nullable', 'string', 'max:120'],
            'title' => ['required', 'string', 'max:180'],
            'description' => ['nullable', 'string', 'max:5000'],
            'objectives' => ['nullable', 'string', 'max:5000'],
            'deliverables' => ['nullable', 'string', 'max:5000'],
            'required_profiles' => ['nullable', 'string', 'max:5000'],
            'man_days' => ['required', 'integer', 'between:1,10000'],
            'visibility' => ['required', Rule::enum(SponsorshipVisibility::class)],
            'cause_ids' => ['sometimes', 'array', 'max:10'],
            'cause_ids.*' => ['integer', 'distinct', 'exists:causes,id'],
            'consent' => ['accepted'],
            'website' => ['nullable', 'max:0'],
        ];
    }

    public function messages(): array
    {
        return [
            'website.max' => 'La soumission a été rejetée.',
            'consent.accepted' => 'Vous devez confirmer que vous êtes autorisé à déposer cette mission.',
        ];
    }
}
