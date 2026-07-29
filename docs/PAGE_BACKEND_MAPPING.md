# First six pages — backend mapping

This document maps each supplied prototype page to its web controller, Blade view, API endpoints, services and database tables.

## 1. Login — `login.html`

### Web

- `GET /connexion`
- `POST /connexion`
- `POST /deconnexion`
- `GET|POST /mot-de-passe-oublie`
- `GET|POST /reinitialiser-mot-de-passe...`
- `GET /auth/google/redirect`
- `GET /auth/linkedin-openid/redirect`
- signed email verification routes

### API

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/register/candidate`
- `POST /api/v1/auth/register/organization`
- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`

### Main code

- `app/Http/Controllers/Web/AuthController.php`
- `app/Http/Controllers/Web/PasswordController.php`
- `app/Http/Controllers/Web/SocialAuthController.php`
- `app/Http/Controllers/Api/V1/AuthController.php`
- `app/Http/Controllers/Api/V1/RegistrationController.php`
- `app/Http/Controllers/Api/V1/PasswordController.php`

### Tables

`users`, `social_accounts`, `personal_access_tokens`, `password_reset_tokens`, `sessions`.

## 2. Public portal — `portail.html`

### Web and API

- `GET /`
- `GET /api/v1/home`

### Dynamic data

- number of published offers;
- number of verified organizations;
- featured/recent offers;
- launch countries;
- sponsor placement.

### Main code

- `app/Services/HomepageService.php`
- `app/Http/Controllers/Api/V1/HomeController.php`
- `resources/views/public/home.blade.php`

### Tables

`offers`, `organizations`, `countries`, `sponsor_slots` and offer taxonomy pivots.

## 3. Missions search — `missions.html`

### Web and API

- `GET /missions`
- `GET /api/v1/offers`

### Supported search

Keyword, country, city/location, engagement type, cause, work mode, duration, language, experience level, date, relevance and proximity-ready sorting.

### Main code

- `app/Services/OfferSearchService.php`
- `app/Http/Requests/OfferIndexRequest.php`
- `app/Http/Controllers/Api/V1/OfferController.php`
- `resources/views/public/offers/index.blade.php`

### Tables

`offers`, `organizations`, `causes`, `cause_offer`, `languages`, `language_offer`, `skills`, `offer_skill`, `countries`.

## 4. NGO directory — `annuaire.html`

### Web and API

- `GET /annuaire`
- `GET /organisations/{slug}`
- `GET /api/v1/organizations`
- `GET /api/v1/organizations/{slug}`

### Supported search

Name/keyword, country, cause, verification level, organization type, size, relevance, name and number of open offers.

### Main code

- `app/Services/OrganizationSearchService.php`
- `app/Http/Requests/OrganizationIndexRequest.php`
- `app/Http/Controllers/Api/V1/OrganizationController.php`
- `resources/views/public/organizations/*`

### Tables

`organizations`, `organization_documents`, `cause_organization`, `countries`, `offers`.

## 5. Skills sponsorship — `mecenat.html`

### Web and API

- `GET /mecenat`
- `POST /mecenat`
- `GET /mecenat/verification/{trackingUuid}`
- `POST /api/v1/sponsorship-missions`
- `GET /api/v1/sponsorship-missions/{trackingUuid}`
- `POST /api/v1/sponsorship-missions/{trackingUuid}/verify`

### Workflow

1. Public submission.
2. Validation, rate limiting and honeypot control.
3. Random tracking UUID and one-time verification token.
4. Verification token stored only as SHA-256.
5. Queued verification notification.
6. Email confirmation moves the mission to `submitted`.
7. Tracking endpoint exposes only safe status data.

### Main code

- `app/Services/SponsorshipMissionService.php`
- `app/Notifications/VerifySponsorshipMission.php`
- `app/Http/Controllers/Web/SponsorshipController.php`
- `app/Http/Controllers/Api/V1/SponsorshipMissionController.php`

### Tables

`sponsorship_missions`, `cause_sponsorship_mission`, `causes`, `countries`, `jobs`, `failed_jobs`.

## 6. Offer detail — `offre.html`

### Web and API

- `GET /missions/{slug}`
- `GET /api/v1/offers/{slug}`
- `GET /api/v1/offers/{slug}/similar`
- `POST /api/v1/offers/{slug}/share`
- `POST /api/v1/offers/{slug}/applications`
- `PUT|DELETE /api/v1/offers/{slug}/saved`
- authenticated web forms for applying and saving/removing favorites

### Dynamic behavior

- full offer and organization data;
- trust badge and taxonomy data;
- view counter;
- similar offers;
- candidate saved/applied state;
- private CV upload;
- duplicate-application prevention;
- share-event analytics without raw IP storage.

### Tables

`offers`, `applications`, `saved_offers`, `offer_events` plus organization and taxonomy tables.

## Cross-cutting controls

- versioned `/api/v1` routes;
- Laravel Sanctum session/token authentication;
- role and verified-email middleware;
- request classes for validation;
- API resources to prevent accidental data exposure;
- database uniqueness for idempotency;
- soft deletion for users, organizations and offers;
- queues for outbound email;
- MySQL, Redis and Mailpit in Docker Compose;
- OpenAPI and Postman documentation;
- Pest feature tests.
