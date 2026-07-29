<?php

namespace App\Http\Controllers\Api\V1;

use App\Enums\AccountStatus;
use App\Enums\UserRole;
use App\Enums\VerificationStatus;
use App\Http\Controllers\Controller;
use App\Http\Requests\Auth\RegisterCandidateRequest;
use App\Http\Requests\Auth\RegisterOrganizationRequest;
use App\Http\Resources\OrganizationResource;
use App\Http\Resources\UserResource;
use App\Models\Organization;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class RegistrationController extends Controller
{
    public function candidate(RegisterCandidateRequest $request): JsonResponse
    {
        $user = User::create([
            ...$request->safe()->except('password_confirmation'),
            'email' => mb_strtolower($request->string('email')->toString()),
            'role' => UserRole::Candidate,
            'status' => AccountStatus::Active,
        ]);

        $user->sendEmailVerificationNotification();

        return response()->json([
            'message' => 'Compte candidat créé. Vérifiez votre adresse e-mail.',
            'data' => new UserResource($user),
        ], 201);
    }

    public function organization(RegisterOrganizationRequest $request): JsonResponse
    {
        [$user, $organization] = DB::transaction(function () use ($request): array {
            $user = User::create([
                'name' => $request->string('owner_name')->toString(),
                'email' => mb_strtolower($request->string('owner_email')->toString()),
                'password' => $request->input('password'),
                'role' => UserRole::OrganizationAdmin,
                'status' => AccountStatus::Active,
            ]);

            $organization = Organization::create([
                'owner_user_id' => $user->id,
                'name' => $request->string('organization_name')->toString(),
                'slug' => Str::slug($request->string('organization_name')->toString()).'-'.Str::lower(Str::random(5)),
                'type' => $request->string('organization_type')->toString(),
                'country_code' => Str::upper($request->string('country_code')->toString()),
                'city' => $request->string('city')->toString(),
                'registry_number' => $request->string('registry_number')->toString(),
                'size' => $request->input('size'),
                'description' => $request->string('description')->toString(),
                'mission' => $request->input('mission'),
                'website' => $request->input('website'),
                'verification_status' => VerificationStatus::Pending,
                'is_active' => true,
            ]);

            $organization->causes()->sync($request->input('cause_ids', []));

            foreach ($request->file('documents', []) as $index => $document) {
                $organization->documents()->create([
                    'type' => $request->input("document_types.$index", 'other'),
                    'file_path' => $document->store("organization-documents/{$organization->id}", 'local'),
                    'status' => 'pending',
                ]);
            }

            return [$user, $organization->fresh(['country', 'causes'])];
        });

        $user->sendEmailVerificationNotification();

        return response()->json([
            'message' => 'Organisation enregistrée et placée en vérification documentaire.',
            'data' => [
                'user' => new UserResource($user),
                'organization' => new OrganizationResource($organization),
            ],
        ], 201);
    }
}
