<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('sponsorship_missions', function (Blueprint $table) {
            $table->id();
            $table->uuid('tracking_uuid')->unique();
            $table->string('contact_email');
            $table->string('company_name', 180);
            $table->string('company_legal_id', 120)->nullable();
            $table->char('country_code', 2)->nullable();
            $table->string('region', 120)->nullable();
            $table->string('title', 180);
            $table->text('description')->nullable();
            $table->text('objectives')->nullable();
            $table->text('deliverables')->nullable();
            $table->text('required_profiles')->nullable();
            $table->unsignedInteger('man_days');
            $table->string('visibility', 40)->default('open')->index();
            $table->string('status', 40)->default('pending_email_verification')->index();
            $table->char('verification_token_hash', 64);
            $table->timestamp('verified_email_at')->nullable();
            $table->timestamp('consent_at');
            $table->string('submitted_ip', 45)->nullable();
            $table->text('user_agent')->nullable();
            $table->timestamps();

            $table->foreign('country_code')->references('code')->on('countries')->nullOnDelete();
            $table->index(['contact_email', 'created_at']);
        });

        Schema::create('cause_sponsorship_mission', function (Blueprint $table) {
            $table->foreignId('cause_id')->constrained()->cascadeOnDelete();
            $table->foreignId('sponsorship_mission_id')->constrained()->cascadeOnDelete();
            $table->primary(['cause_id', 'sponsorship_mission_id']);
        });

        Schema::create('sponsor_slots', function (Blueprint $table) {
            $table->id();
            $table->string('placement', 80)->index();
            $table->string('sponsor_name', 180);
            $table->string('label', 80)->default('Partenariat');
            $table->text('copy');
            $table->string('target_url')->nullable();
            $table->timestamp('starts_at')->nullable();
            $table->timestamp('ends_at')->nullable();
            $table->boolean('is_active')->default(true)->index();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('sponsor_slots');
        Schema::dropIfExists('cause_sponsorship_mission');
        Schema::dropIfExists('sponsorship_missions');
    }
};
