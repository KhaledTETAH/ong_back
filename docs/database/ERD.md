# Entity relationship diagram

```mermaid
erDiagram
    USERS ||--o{ SOCIAL_ACCOUNTS : owns
    USERS ||--o{ ORGANIZATIONS : owns
    USERS ||--o{ APPLICATIONS : submits
    USERS ||--o{ SAVED_OFFERS : saves
    USERS ||--o{ OFFER_EVENTS : triggers

    COUNTRIES ||--o{ ORGANIZATIONS : locates
    COUNTRIES ||--o{ OFFERS : locates
    COUNTRIES ||--o{ SPONSORSHIP_MISSIONS : locates

    ORGANIZATIONS ||--o{ ORGANIZATION_DOCUMENTS : verifies_with
    ORGANIZATIONS ||--o{ OFFERS : publishes
    ORGANIZATIONS }o--o{ CAUSES : supports

    OFFERS }o--o{ CAUSES : classified_by
    OFFERS }o--o{ LANGUAGES : requires
    OFFERS }o--o{ SKILLS : requires
    OFFERS ||--o{ APPLICATIONS : receives
    OFFERS ||--o{ SAVED_OFFERS : bookmarked_as
    OFFERS ||--o{ OFFER_EVENTS : measured_by

    SPONSORSHIP_MISSIONS }o--o{ CAUSES : targets

    USERS {
        bigint id PK
        string name
        string email UK
        string password
        string role
        string status
        timestamp email_verified_at
    }

    ORGANIZATIONS {
        bigint id PK
        bigint owner_user_id FK
        string name
        string slug UK
        string type
        char country_code FK
        string city
        string verification_status
        boolean is_active
    }

    OFFERS {
        bigint id PK
        bigint organization_id FK
        uuid uuid UK
        string slug UK
        string title
        string engagement_type
        char country_code FK
        string city
        string remote_mode
        string status
        timestamp published_at
        timestamp expires_at
    }

    SPONSORSHIP_MISSIONS {
        bigint id PK
        uuid tracking_uuid UK
        string contact_email
        string company_name
        string title
        int man_days
        string visibility
        string status
        char verification_token_hash
    }

    APPLICATIONS {
        bigint id PK
        bigint offer_id FK
        bigint candidate_id FK
        string status
        timestamp applied_at
    }
```

## Design rules

- Human-facing URLs use stable unique slugs.
- External/private tracking uses UUIDs.
- User roles and statuses are strings cast to PHP enums.
- Many-to-many taxonomies avoid duplicated text in organizations and offers.
- Uploaded verification documents and CVs are stored privately.
- Searchable columns have targeted indexes; pivot foreign keys are composite primary keys.
- Applications and saved offers use database uniqueness to enforce idempotency.
