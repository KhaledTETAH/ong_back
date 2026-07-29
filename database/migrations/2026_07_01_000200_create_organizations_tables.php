<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('organizations', function (Blueprint $table) {
            $table->id();
            $table->foreignId('owner_user_id')->nullable()->constrained('users')->nullOnDelete();
            $table->string('name', 180);
            $table->string('slug', 200)->unique();
            $table->string('type', 40)->index();
            $table->char('country_code', 2);
            $table->string('city', 120);
            $table->string('address')->nullable();
            $table->decimal('latitude', 10, 7)->nullable();
            $table->decimal('longitude', 10, 7)->nullable();
            $table->string('registry_number', 120)->nullable();
            $table->string('size', 30)->nullable()->index();
            $table->text('description');
            $table->text('mission')->nullable();
            $table->string('verification_status', 30)->default('pending')->index();
            $table->timestamp('verified_at')->nullable();
            $table->string('logo_path')->nullable();
            $table->string('website')->nullable();
            $table->unsignedSmallInteger('founded_year')->nullable();
            $table->unsignedInteger('volunteer_count')->default(0);
            $table->boolean('is_active')->default(true)->index();
            $table->timestamps();
            $table->softDeletes();

            $table->foreign('country_code')->references('code')->on('countries')->restrictOnDelete();
            $table->index(['country_code', 'city']);
            $table->index(['verification_status', 'is_active']);
        });

        Schema::create('cause_organization', function (Blueprint $table) {
            $table->foreignId('cause_id')->constrained()->cascadeOnDelete();
            $table->foreignId('organization_id')->constrained()->cascadeOnDelete();
            $table->primary(['cause_id', 'organization_id']);
        });

        Schema::create('organization_documents', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->cascadeOnDelete();
            $table->string('type', 60)->index();
            $table->string('file_path');
            $table->string('status', 30)->default('pending')->index();
            $table->foreignId('reviewed_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('reviewed_at')->nullable();
            $table->text('rejection_reason')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('organization_documents');
        Schema::dropIfExists('cause_organization');
        Schema::dropIfExists('organizations');
    }
};
