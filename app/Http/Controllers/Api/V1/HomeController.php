<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Resources\OfferSummaryResource;
use App\Services\HomepageService;
use Illuminate\Http\JsonResponse;

class HomeController extends Controller
{
    public function __invoke(HomepageService $homepage): JsonResponse
    {
        $data = $homepage->data();

        return response()->json([
            'data' => [
                'stats' => $data['stats'],
                'featured_offers' => OfferSummaryResource::collection($data['featured_offers']),
                'coverage_countries' => $data['coverage_countries'],
                'sponsor' => $data['sponsor'],
            ],
        ]);
    }
}
