<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\OrganizationIndexRequest;
use App\Http\Resources\OrganizationResource;
use App\Http\Resources\OrganizationSummaryResource;
use App\Models\Organization;
use App\Services\OrganizationSearchService;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class OrganizationController extends Controller
{
    public function index(
        OrganizationIndexRequest $request,
        OrganizationSearchService $search
    ): AnonymousResourceCollection {
        return OrganizationSummaryResource::collection(
            $search->search($request->validated())
        );
    }

    public function show(Organization $organization): OrganizationResource
    {
        abort_unless($organization->is_active, 404);

        $organization->load([
            'country',
            'causes',
            'offers' => fn ($query) => $query->published()->with('country')->latest('published_at')->limit(20),
        ]);

        return new OrganizationResource($organization);
    }
}
