<?php

namespace App\Http\Requests\Auth;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class RegisterOrganizationRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'owner_name' => ['required', 'string', 'max:160'],
            'owner_email' => ['required', 'email:rfc', 'max:255', 'unique:users,email'],
            'password' => ['required', 'confirmed', Password::min(10)->mixedCase()->numbers()],
            'organization_name' => ['required', 'string', 'max:180'],
            'organization_type' => ['required', 'in:association,foundation,ngo,waqf'],
            'country_code' => ['required', 'string', 'size:2', 'exists:countries,code'],
            'city' => ['required', 'string', 'max:120'],
            'registry_number' => ['required', 'string', 'max:120'],
            'size' => ['nullable', 'in:micro,small,medium,large'],
            'description' => ['required', 'string', 'max:5000'],
            'mission' => ['nullable', 'string', 'max:5000'],
            'website' => ['nullable', 'url:http,https', 'max:255'],
            'cause_ids' => ['required', 'array', 'min:1', 'max:10'],
            'cause_ids.*' => ['integer', 'distinct', 'exists:causes,id'],
            'documents' => ['sometimes', 'array', 'max:5'],
            'documents.*' => ['file', 'mimes:pdf,jpg,jpeg,png', 'max:10240'],
            'document_types' => ['sometimes', 'array'],
            'document_types.*' => ['string', 'in:statutes,registration_receipt,activity_report,accreditation,other'],
        ];
    }
}
