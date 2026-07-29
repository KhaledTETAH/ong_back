# Database documentation

## Canonical source

Laravel migrations in `database/migrations` are the canonical schema. Run:

```bash
php artisan migrate
php artisan db:seed
```

## Tables

### Identity

#### `users`

Authentication identity shared by candidates, organization staff, moderators and platform administrators.

Important constraints:

- unique `email`;
- soft deletion;
- indexed `role` and `status`;
- nullable password to allow social-only accounts.

#### `social_accounts`

Maps a provider identity to one local user. Provider tokens are encrypted by Laravel casts and never returned by API resources.

#### `personal_access_tokens`

Sanctum bearer tokens. Only token hashes are stored.

#### `password_reset_tokens`, `sessions`

Standard Laravel authentication support.

### Reference data

#### `countries`

ISO alpha-2 code primary key. `is_covered` identifies the six launch countries.

#### `causes`

Shared classification for organizations, offers and sponsorship missions.

#### `languages`

Required languages attached to offers.

#### `skills`

Structured skills attached to offers. `offer_skill.is_required` distinguishes required and optional skills.

### Organizations

#### `organizations`

Public and operational organization identity.

Key columns:

- `type`: association, foundation, NGO or Waqf;
- `verification_status`: pending, verified, Certified+ or rejected;
- `is_active`: administrative visibility switch;
- coordinates for future proximity search;
- registry and public transparency information.

Public directory queries always require active plus verified/Certified+.

#### `organization_documents`

Private KYB files. Review status and reviewer are auditable.

#### `cause_organization`

Organization-to-cause many-to-many pivot.

### Offers

#### `offers`

All engagement formats are represented in one table through `engagement_type`.

Publication visibility requires:

- status `published`;
- non-null `published_at`;
- no expiry or expiry later than the current time.

`duration_days` supports filtering while `duration_label` preserves user-friendly text such as “10 jours-homme” or “Mandat 2 ans”.

#### `cause_offer`, `language_offer`, `offer_skill`

Searchable classifications.

#### `applications`

A candidate application. Unique `(offer_id, candidate_id)` prevents duplicates.

#### `saved_offers`

Unique bookmark pivot.

#### `offer_events`

Lightweight analytics for share events and future view/click events. Raw IP and user agent are not stored; only hashes.

### Skills sponsorship

#### `sponsorship_missions`

Company-side submission without a full enterprise account.

Security fields:

- random tracking UUID;
- SHA-256 email-verification token hash;
- private IP and user-agent metadata;
- consent timestamp.

Workflow:

```text
pending_email_verification
→ submitted
→ under_review
→ matched
→ in_progress
→ completed
```

#### `cause_sponsorship_mission`

Target causes.

### Content and operations

#### `sponsor_slots`

Controls non-intrusive sponsor content by placement and active dates.

#### `cache`, `jobs`, `failed_jobs`, `job_batches`

Laravel infrastructure for caching and queued email notifications.

## Indexing

Existing indexes cover:

- user role/status;
- organization country/city, verification and activity;
- offer status/publication date, country/city, featured status, engagement type and mode;
- sponsorship status, visibility, email and creation date;
- application status;
- analytics event type and creation date.

For high-volume production search, add one of:

1. MySQL full-text indexes for title/description/profile fields;
2. Meilisearch through Laravel Scout;
3. Elasticsearch/OpenSearch for multilingual stemming and geospatial ranking.

The current implementation intentionally keeps SQL search portable and deterministic.

## Data retention recommendations

- Rejected sponsorship submissions: delete or anonymize after 12 months.
- Offer-event hashes: aggregate and delete raw rows after 90 days.
- Unverified accounts: purge after 30–90 days.
- Organization verification files: retain according to legal and KYB policy.
- Candidate CVs: delete when the application-retention period expires.
