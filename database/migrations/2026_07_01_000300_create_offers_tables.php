<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('offers', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->cascadeOnDelete();
            $table->uuid('uuid')->unique();
            $table->string('slug', 220)->unique();
            $table->string('title', 180);
            $table->string('engagement_type', 40)->index();
            $table->string('employment_contract', 30)->nullable()->index();
            $table->char('country_code', 2);
            $table->string('region', 120)->nullable();
            $table->string('city', 120);
            $table->string('address')->nullable();
            $table->decimal('latitude', 10, 7)->nullable();
            $table->decimal('longitude', 10, 7)->nullable();
            $table->string('remote_mode', 20)->index();
            $table->longText('description');
            $table->longText('responsibilities')->nullable();
            $table->longText('desired_profile')->nullable();
            $table->longText('conditions')->nullable();
            $table->string('duration_label', 100)->nullable();
            $table->unsignedInteger('duration_days')->nullable();
            $table->date('start_date')->nullable();
            $table->date('end_date')->nullable();
            $table->string('experience_level', 30)->nullable()->index();
            $table->string('status', 30)->default('draft')->index();
            $table->timestamp('published_at')->nullable()->index();
            $table->timestamp('expires_at')->nullable()->index();
            $table->string('contact_email')->nullable();
            $table->boolean('featured')->default(false)->index();
            $table->unsignedBigInteger('views_count')->default(0);
            $table->timestamps();
            $table->softDeletes();

            $table->foreign('country_code')->references('code')->on('countries')->restrictOnDelete();
            $table->index(['status', 'published_at']);
            $table->index(['country_code', 'city']);
            $table->index(['featured', 'status', 'published_at']);
        });

        Schema::create('cause_offer', function (Blueprint $table) {
            $table->foreignId('cause_id')->constrained()->cascadeOnDelete();
            $table->foreignId('offer_id')->constrained()->cascadeOnDelete();
            $table->primary(['cause_id', 'offer_id']);
        });

        Schema::create('language_offer', function (Blueprint $table) {
            $table->foreignId('language_id')->constrained()->cascadeOnDelete();
            $table->foreignId('offer_id')->constrained()->cascadeOnDelete();
            $table->primary(['language_id', 'offer_id']);
        });

        Schema::create('offer_skill', function (Blueprint $table) {
            $table->foreignId('offer_id')->constrained()->cascadeOnDelete();
            $table->foreignId('skill_id')->constrained()->cascadeOnDelete();
            $table->boolean('is_required')->default(true);
            $table->primary(['offer_id', 'skill_id']);
        });

        Schema::create('applications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('offer_id')->constrained()->cascadeOnDelete();
            $table->foreignId('candidate_id')->constrained('users')->cascadeOnDelete();
            $table->longText('cover_letter')->nullable();
            $table->string('cv_path')->nullable();
            $table->string('status', 30)->default('new')->index();
            $table->timestamp('applied_at');
            $table->timestamp('withdrawn_at')->nullable();
            $table->timestamps();
            $table->unique(['offer_id', 'candidate_id']);
        });

        Schema::create('saved_offers', function (Blueprint $table) {
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('offer_id')->constrained()->cascadeOnDelete();
            $table->timestamp('created_at')->useCurrent();
            $table->primary(['user_id', 'offer_id']);
        });

        Schema::create('offer_events', function (Blueprint $table) {
            $table->id();
            $table->foreignId('offer_id')->constrained()->cascadeOnDelete();
            $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
            $table->string('event_type', 30)->index();
            $table->string('channel', 30)->nullable();
            $table->char('ip_hash', 64)->nullable();
            $table->char('user_agent_hash', 64)->nullable();
            $table->timestamp('created_at')->useCurrent()->index();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('offer_events');
        Schema::dropIfExists('saved_offers');
        Schema::dropIfExists('applications');
        Schema::dropIfExists('offer_skill');
        Schema::dropIfExists('language_offer');
        Schema::dropIfExists('cause_offer');
        Schema::dropIfExists('offers');
    }
};
