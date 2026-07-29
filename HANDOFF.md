# Technical handoff

## Delivery status

The repository contains the complete backend and dynamic server-rendered integration for prototype pages 1–6. It is intended as the first production-grade slice of the wider Engagement Platform specification.

## What is ready

- Laravel application skeleton and environment configuration.
- Session authentication and versioned Sanctum REST API.
- Candidate and organization registration APIs.
- Password reset and email verification.
- Google and LinkedIn OpenID hooks.
- Dynamic public home page.
- Searchable and paginated mission catalogue.
- Searchable and paginated organization directory.
- Public organization profiles.
- Skills-sponsorship mission submission and verification workflow.
- Offer detail, similar offers, view counting, apply, save and share behavior.
- Normalized migrations, seed data and MySQL reference schema.
- OpenAPI specification and Postman collection.
- Docker Compose development environment.
- Feature tests and PHP syntax validation.

## Required setup before a real deployment

1. Run `composer install` and commit the generated `composer.lock` after dependency resolution.
2. Configure production database, Redis, mail provider and application key.
3. Register Google/LinkedIn OAuth applications and configure callback URLs.
4. Replace Mailpit with a transactional email provider.
5. Configure HTTPS, trusted proxies, secure cookies and secrets management.
6. Configure object/private storage and malware scanning for uploaded CVs/documents.
7. Run migrations, tests and a dependency/security audit in CI.
8. Configure a persistent queue worker and scheduled backup jobs.

## Validation checklist

- Build the Docker image with `docker compose build`.
- Start the stack with `docker compose up -d`.
- Generate the application key with `php artisan key:generate`.
- Run migrations and seed data with `php artisan migrate --seed`.
- Run the feature test suite with `php artisan test`.
- Smoke-test the public pages and `/api/v1` endpoints.

## Runtime notes

The production Docker image installs runtime dependencies only. Install development dependencies when running Pest or local quality checks.
