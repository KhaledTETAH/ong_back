# REST API reference

## Conventions

Base path:

```text
/api/v1
```

All JSON requests should send:

```http
Accept: application/json
Content-Type: application/json
```

Protected endpoints require:

```http
Authorization: Bearer <token>
```

Successful list responses use Laravel resource pagination:

```json
{
  "data": [],
  "links": {
    "first": "http://localhost:8000/api/v1/offers?page=1",
    "last": "http://localhost:8000/api/v1/offers?page=3",
    "prev": null,
    "next": "http://localhost:8000/api/v1/offers?page=2"
  },
  "meta": {
    "current_page": 1,
    "from": 1,
    "last_page": 3,
    "per_page": 12,
    "to": 12,
    "total": 29
  }
}
```

Validation failure:

```json
{
  "message": "The given data was invalid.",
  "errors": {
    "email": ["The email field is required."]
  }
}
```

## Authentication

### POST `/auth/login`

Request:

```json
{
  "email": "candidat@example.test",
  "password": "Password123!",
  "device_name": "Web frontend"
}
```

Response `200`:

```json
{
  "data": {
    "user": {
      "id": 1,
      "name": "Nadia Benali",
      "email": "candidat@example.test",
      "role": "candidate",
      "status": "active"
    },
    "token": "1|plain-text-token-shown-once",
    "token_type": "Bearer"
  }
}
```

Rate limit: 5 attempts per minute per email and IP.

### GET `/auth/me`

Requires Sanctum. Returns the authenticated user.

### POST `/auth/logout`

Requires Sanctum. Revokes the current token only.

### POST `/auth/register/candidate`

```json
{
  "name": "Samira Test",
  "email": "samira@example.test",
  "phone": "+213555000000",
  "password": "StrongPassword123!",
  "password_confirmation": "StrongPassword123!",
  "locale": "fr"
}
```

Creates a candidate and sends an email-verification notification.

### POST `/auth/register/organization`

Use `multipart/form-data`.

Fields:

| Field | Required | Notes |
|---|---:|---|
| `owner_name` | yes | Account owner |
| `owner_email` | yes | Unique |
| `password` | yes | Minimum 10, mixed case and number |
| `password_confirmation` | yes | |
| `organization_name` | yes | |
| `organization_type` | yes | `association`, `foundation`, `ngo`, `waqf` |
| `country_code` | yes | ISO alpha-2 |
| `city` | yes | |
| `registry_number` | yes | Official identifier |
| `size` | no | `micro`, `small`, `medium`, `large` |
| `description` | yes | |
| `mission` | no | |
| `website` | no | HTTPS or HTTP URL |
| `cause_ids[]` | yes | Existing cause IDs |
| `documents[]` | no | PDF/JPG/PNG, max 10 MB each |
| `document_types[]` | no | Type aligned with each document |

The organization is created with verification status `pending`.

### POST `/auth/forgot-password`

```json
{
  "email": "candidat@example.test"
}
```

Always returns a neutral response to avoid account enumeration.

### POST `/auth/reset-password`

```json
{
  "email": "candidat@example.test",
  "token": "reset-token",
  "password": "NewPassword123!",
  "password_confirmation": "NewPassword123!"
}
```

## Homepage

### GET `/home`

Returns:

- live count of open offers;
- live count of verified organizations;
- four featured/recent offers;
- covered countries;
- current sponsor placement.

## Offers

### GET `/offers`

Query parameters:

| Parameter | Type | Example | Behavior |
|---|---|---|---|
| `q` | string | `Laravel` | Searches title, description, desired profile, responsibilities, organization, causes and skills |
| `location` | string | `Oran` | City, region or country name |
| `country` | ISO code | `DZ` | Exact country |
| `city` | string | `Oran` | City filter |
| `type` | enum | `volunteering` | Engagement type |
| `cause` | slug | `education` | Cause |
| `mode[]` | enum[] | `remote` | `on_site`, `hybrid`, `remote` |
| `duration` | enum | `short` | `short` ≤ 30 days, `medium` 31–180, `long` > 180 |
| `language` | code | `fr` | Language |
| `experience_level` | enum | `confirmed` | `junior`, `confirmed`, `senior`, `expert`, `governance` |
| `sort` | enum | `recent` | `relevance`, `recent`, `oldest`, `proximity` |
| `lat` | number | `35.6971` | Required for distance calculation |
| `lng` | number | `-0.6308` | Required for distance calculation |
| `radius_km` | integer | `50` | MySQL geospatial-radius filter |
| `page` | integer | `1` | |
| `per_page` | integer | `12` | Maximum 50 |

Example:

```http
GET /api/v1/offers?q=education&country=DZ&mode[]=on_site&sort=relevance
```

### GET `/offers/{slug}`

Returns the complete offer:

- organization and trust badge;
- location and engagement metadata;
- causes, languages and skills;
- description;
- responsibilities;
- desired profile;
- conditions;
- dates and duration;
- authenticated candidate state: `is_saved`, `has_applied`.

A view counter is incremented.

### GET `/offers/{slug}/similar`

Returns up to six published offers sharing the engagement type or at least one cause.

### POST `/offers/{slug}/share`

Public endpoint.

```json
{
  "channel": "linkedin"
}
```

Allowed channels: `copy_link`, `email`, `linkedin`, `facebook`, `whatsapp`, `other`.

The API stores only SHA-256 hashes of IP and user agent for lightweight analytics.

### POST `/offers/{slug}/applications`

Requires a candidate token. Accepts JSON or `multipart/form-data`.

```json
{
  "cover_letter": "Je souhaite contribuer à cette mission."
}
```

Optional `cv`: PDF/DOC/DOCX, maximum 5 MB. The CV is private.

The pair `(offer_id, candidate_id)` is unique, so a candidate cannot apply twice.

### PUT `/offers/{slug}/saved`

Requires a candidate token. Idempotently saves the offer.

### DELETE `/offers/{slug}/saved`

Requires a candidate token. Removes the saved offer.

## Organizations

### GET `/organizations`

Query parameters:

| Parameter | Example |
|---|---|
| `q` | `éducation` |
| `country` | `DZ` |
| `cause` | `education` |
| `verification[]` | `verified`, `certified_plus` |
| `type` | `association`, `foundation`, `ngo`, `waqf` |
| `size` | `micro`, `small`, `medium`, `large` |
| `sort` | `relevance`, `name`, `offers` |
| `page` | `1` |
| `per_page` | `12` |

Only active, verified or Certified+ organizations are public.

### GET `/organizations/{slug}`

Returns the public organization profile with causes and up to 20 open offers.

## Skills sponsorship

### POST `/sponsorship-missions`

Public, rate-limited to five submissions per hour per IP.

```json
{
  "contact_email": "mecenat@company.test",
  "company_name": "Entreprise Solidaire",
  "company_legal_id": "RC-2026-001",
  "country_code": "FR",
  "region": "Île-de-France",
  "title": "Audit de cybersécurité solidaire",
  "description": "Audit et plan de remédiation.",
  "objectives": "Réduire les risques prioritaires.",
  "deliverables": "Rapport, feuille de route, restitution.",
  "required_profiles": "Consultant cybersécurité senior.",
  "man_days": 12,
  "visibility": "verified_organizations",
  "cause_ids": [2],
  "consent": true,
  "website": ""
}
```

`website` is a honeypot and must remain empty.

Response `201` returns a tracking UUID. In local/test environments only, `debug_verification_token` is returned to simplify testing. Production never exposes it.

### POST `/sponsorship-missions/{trackingUuid}/verify`

```json
{
  "token": "plain-email-verification-token"
}
```

Changes status from `pending_email_verification` to `submitted`.

### GET `/sponsorship-missions/{trackingUuid}?token=...`

Returns the mission to the holder of the original tracking token.

## Enumerations

### Engagement type

```text
volunteering
employment
freelance
consulting
governance
skills_sponsorship
```

### Remote mode

```text
on_site
hybrid
remote
```

### Organization verification

```text
pending
verified
certified_plus
rejected
```

### Sponsorship visibility

```text
open
verified_organizations
confidential
```

### Sponsorship status

```text
pending_email_verification
submitted
under_review
matched
in_progress
completed
rejected
```

### Application status

```text
new
pre_qualified
interview
decision
offer
accepted
rejected
talent_pool
withdrawn
```
