# Engagement Platform — Laravel backend for the first six pages

This repository turns the first six static pages of the supplied `ong-theme` prototype into a database-backed Laravel application and a versioned REST API.

## Implemented scope

| Prototype page | Dynamic backend coverage |
|---|---|
| 1. Login | Session login, Sanctum token login, logout, browser/API password reset, email verification, candidate and organization registration APIs, Google and LinkedIn OpenID integration points |
| 2. Public portal | Live statistics, featured offers, covered countries, sponsor placement |
| 3. Missions | Keyword search, filters, sorting, geolocation-ready proximity search, pagination |
| 4. NGO directory | Search, country/cause/verification/type/size filters, sorting, organization detail |
| 5. Skills sponsorship | Secure mission submission, email verification, tracking token, anti-spam honeypot, queued notification |
| 6. Offer detail | Full offer data, organization card, similar offers, views, functional browser apply/save actions, and apply/save/share API endpoints |

The original visual style is preserved in dynamic Blade templates under `resources/views`, while the source CSS is under `public/css`.

## Stack

- Laravel 13
- PHP 8.3+
- MySQL 8.4
- Redis 7.4
- Laravel Sanctum
- Laravel Socialite
- Blade + Bootstrap 5
- Pest 4
- Docker Compose, Nginx, Mailpit

## Quick start with Docker

```bash
cp .env.example .env
docker compose build
docker compose run --rm app php artisan key:generate
docker compose up -d
docker compose exec app php artisan migrate --seed
docker compose exec app php artisan storage:link
```

Open:

- Website: `http://localhost:8000`
- Mailpit: `http://localhost:8025`

Demo accounts:

```text
Candidate:
candidat@example.test
Password123!

Organization administrator:
organisation@example.test
Password123!
```

## Local start without Docker

Requirements: PHP 8.3+, Composer 2, MySQL or SQLite.

```bash
composer install
cp .env.example .env
php artisan key:generate
touch database/database.sqlite
```

For SQLite, change `.env`:

```dotenv
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database/database.sqlite
CACHE_STORE=database
QUEUE_CONNECTION=database
SESSION_DRIVER=database
```

Then:

```bash
php artisan migrate --seed
php artisan storage:link
php artisan serve
php artisan queue:work
```

## API

Base URL:

```text
/api/v1
```

Authentication:

```http
Authorization: Bearer <sanctum-token>
Accept: application/json
```

Documentation files:

- `HANDOFF.md`
- `docs/PAGE_BACKEND_MAPPING.md`
- `docs/API_REFERENCE.md`
- `docs/openapi.yaml`
- `docs/postman_collection.json`
- `docs/database/ERD.md`
- `docs/database/DATABASE.md`
- `docs/database/schema.sql`
- `docs/SECURITY.md`
- `docs/DEPLOYMENT.md`

## Main API groups

```text
POST   /api/v1/auth/login
POST   /api/v1/auth/register/candidate
POST   /api/v1/auth/register/organization
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/auth/me
POST   /api/v1/auth/logout

GET    /api/v1/home
GET    /api/v1/offers
GET    /api/v1/offers/{slug}
GET    /api/v1/offers/{slug}/similar
POST   /api/v1/offers/{slug}/share
POST   /api/v1/offers/{slug}/applications
PUT    /api/v1/offers/{slug}/saved
DELETE /api/v1/offers/{slug}/saved

GET    /api/v1/organizations
GET    /api/v1/organizations/{slug}

POST   /api/v1/sponsorship-missions
GET    /api/v1/sponsorship-missions/{trackingUuid}
POST   /api/v1/sponsorship-missions/{trackingUuid}/verify
```

## Database strategy

The schema is normalized around:

- identities and authentication;
- organizations and verification;
- taxonomies such as causes, languages and skills;
- offers and searchable relations;
- applications and saved offers;
- skills-sponsorship submissions and email verification;
- sponsor placements and event analytics.

Laravel migrations are the canonical source of truth. The SQL file is included as a readable MySQL reference, not as a replacement for migrations.

## Tests

```bash
php artisan test
```

The feature suite covers:

- authentication;
- candidate registration;
- offer search and detail;
- organization directory and detail;
- sponsorship submission;
- applying and saving offers;
- rendering the six public pages;
- browser-based password reset request;
- browser-based application and favorite actions.

## Security notes

- Passwords are hashed through Laravel's `hashed` cast.
- API tokens are managed by Sanctum and stored hashed.
- Login and public-write endpoints are rate-limited.
- Sponsorship submissions use validation, a honeypot and email confirmation.
- Sensitive organization documents and candidate CVs use the private storage disk.
- Public responses never expose contact email, IP address, verification hashes or provider tokens.
- Production should use HTTPS, secure cookies, managed secrets, backups and malware scanning for uploaded documents.

## Arabic summary

هذا المشروع يحوّل أول ست صفحات من التصميم الثابت إلى تطبيق Laravel فعلي مرتبط بقاعدة بيانات، مع REST API موثّق. يشمل تسجيل الدخول، الصفحة العامة، البحث عن المهمات، دليل الجمعيات، إرسال مهمات التبرع بالمهارات، وتفاصيل العرض، بالإضافة إلى التقديم والحفظ والتتبع.


## Validation note

Run `composer install`, `php artisan test`, and `docker compose build` before release or deployment. See `HANDOFF.md` for the full setup and verification checklist.
