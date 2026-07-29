-- MySQL 8.4 reference schema
-- Canonical schema: Laravel migrations under database/migrations.
-- Charset: utf8mb4 / collation: utf8mb4_unicode_ci.

CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    email_verified_at TIMESTAMP NULL,
    phone VARCHAR(40) NULL,
    password VARCHAR(255) NULL,
    role VARCHAR(40) NOT NULL DEFAULT 'candidate',
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    locale VARCHAR(10) NOT NULL DEFAULT 'fr',
    last_login_at TIMESTAMP NULL,
    last_login_ip VARCHAR(45) NULL,
    remember_token VARCHAR(100) NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL,
    INDEX users_role_index (role),
    INDEX users_status_index (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE social_accounts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    provider VARCHAR(40) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    provider_email VARCHAR(255) NULL,
    access_token TEXT NULL,
    refresh_token TEXT NULL,
    token_expires_at TIMESTAMP NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    UNIQUE KEY social_provider_identity_unique (provider, provider_user_id),
    CONSTRAINT social_accounts_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,
    name_fr VARCHAR(100) NOT NULL,
    is_covered TINYINT(1) NOT NULL DEFAULT 0,
    sort_order SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    INDEX countries_covered_index (is_covered)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE causes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(140) NOT NULL UNIQUE,
    description TEXT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    sort_order SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    INDEX causes_active_index (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE languages (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    name_fr VARCHAR(80) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    INDEX languages_active_index (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE skills (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(140) NOT NULL UNIQUE,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    INDEX skills_active_index (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE organizations (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    owner_user_id BIGINT UNSIGNED NULL,
    name VARCHAR(180) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    type VARCHAR(40) NOT NULL,
    country_code CHAR(2) NOT NULL,
    city VARCHAR(120) NOT NULL,
    address VARCHAR(255) NULL,
    latitude DECIMAL(10,7) NULL,
    longitude DECIMAL(10,7) NULL,
    registry_number VARCHAR(120) NULL,
    size VARCHAR(30) NULL,
    description TEXT NOT NULL,
    mission TEXT NULL,
    verification_status VARCHAR(30) NOT NULL DEFAULT 'pending',
    verified_at TIMESTAMP NULL,
    logo_path VARCHAR(255) NULL,
    website VARCHAR(255) NULL,
    founded_year SMALLINT UNSIGNED NULL,
    volunteer_count INT UNSIGNED NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL,
    INDEX organizations_type_index (type),
    INDEX organizations_size_index (size),
    INDEX organizations_country_city_index (country_code, city),
    INDEX organizations_verification_active_index (verification_status, is_active),
    CONSTRAINT organizations_owner_fk FOREIGN KEY (owner_user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT organizations_country_fk FOREIGN KEY (country_code) REFERENCES countries(code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE cause_organization (
    cause_id BIGINT UNSIGNED NOT NULL,
    organization_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (cause_id, organization_id),
    CONSTRAINT cause_organization_cause_fk FOREIGN KEY (cause_id) REFERENCES causes(id) ON DELETE CASCADE,
    CONSTRAINT cause_organization_org_fk FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE organization_documents (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    organization_id BIGINT UNSIGNED NOT NULL,
    type VARCHAR(60) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    reviewed_by BIGINT UNSIGNED NULL,
    reviewed_at TIMESTAMP NULL,
    rejection_reason TEXT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    INDEX organization_documents_type_index (type),
    INDEX organization_documents_status_index (status),
    CONSTRAINT organization_documents_org_fk FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    CONSTRAINT organization_documents_reviewer_fk FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE offers (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    organization_id BIGINT UNSIGNED NOT NULL,
    uuid CHAR(36) NOT NULL UNIQUE,
    slug VARCHAR(220) NOT NULL UNIQUE,
    title VARCHAR(180) NOT NULL,
    engagement_type VARCHAR(40) NOT NULL,
    employment_contract VARCHAR(30) NULL,
    country_code CHAR(2) NOT NULL,
    region VARCHAR(120) NULL,
    city VARCHAR(120) NOT NULL,
    address VARCHAR(255) NULL,
    latitude DECIMAL(10,7) NULL,
    longitude DECIMAL(10,7) NULL,
    remote_mode VARCHAR(20) NOT NULL,
    description LONGTEXT NOT NULL,
    responsibilities LONGTEXT NULL,
    desired_profile LONGTEXT NULL,
    conditions LONGTEXT NULL,
    duration_label VARCHAR(100) NULL,
    duration_days INT UNSIGNED NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    experience_level VARCHAR(30) NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'draft',
    published_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL,
    contact_email VARCHAR(255) NULL,
    featured TINYINT(1) NOT NULL DEFAULT 0,
    views_count BIGINT UNSIGNED NOT NULL DEFAULT 0,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL,
    INDEX offers_engagement_type_index (engagement_type),
    INDEX offers_contract_index (employment_contract),
    INDEX offers_remote_mode_index (remote_mode),
    INDEX offers_experience_index (experience_level),
    INDEX offers_status_published_index (status, published_at),
    INDEX offers_country_city_index (country_code, city),
    INDEX offers_featured_status_published_index (featured, status, published_at),
    CONSTRAINT offers_organization_fk FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    CONSTRAINT offers_country_fk FOREIGN KEY (country_code) REFERENCES countries(code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE cause_offer (
    cause_id BIGINT UNSIGNED NOT NULL,
    offer_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (cause_id, offer_id),
    CONSTRAINT cause_offer_cause_fk FOREIGN KEY (cause_id) REFERENCES causes(id) ON DELETE CASCADE,
    CONSTRAINT cause_offer_offer_fk FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE language_offer (
    language_id BIGINT UNSIGNED NOT NULL,
    offer_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (language_id, offer_id),
    CONSTRAINT language_offer_language_fk FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE CASCADE,
    CONSTRAINT language_offer_offer_fk FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE offer_skill (
    offer_id BIGINT UNSIGNED NOT NULL,
    skill_id BIGINT UNSIGNED NOT NULL,
    is_required TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (offer_id, skill_id),
    CONSTRAINT offer_skill_offer_fk FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE,
    CONSTRAINT offer_skill_skill_fk FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE applications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    offer_id BIGINT UNSIGNED NOT NULL,
    candidate_id BIGINT UNSIGNED NOT NULL,
    cover_letter LONGTEXT NULL,
    cv_path VARCHAR(255) NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'new',
    applied_at TIMESTAMP NOT NULL,
    withdrawn_at TIMESTAMP NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    UNIQUE KEY applications_offer_candidate_unique (offer_id, candidate_id),
    INDEX applications_status_index (status),
    CONSTRAINT applications_offer_fk FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE,
    CONSTRAINT applications_candidate_fk FOREIGN KEY (candidate_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE saved_offers (
    user_id BIGINT UNSIGNED NOT NULL,
    offer_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, offer_id),
    CONSTRAINT saved_offers_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT saved_offers_offer_fk FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE offer_events (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    offer_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NULL,
    event_type VARCHAR(30) NOT NULL,
    channel VARCHAR(30) NULL,
    ip_hash CHAR(64) NULL,
    user_agent_hash CHAR(64) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX offer_events_type_index (event_type),
    INDEX offer_events_created_index (created_at),
    CONSTRAINT offer_events_offer_fk FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE,
    CONSTRAINT offer_events_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE sponsorship_missions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tracking_uuid CHAR(36) NOT NULL UNIQUE,
    contact_email VARCHAR(255) NOT NULL,
    company_name VARCHAR(180) NOT NULL,
    company_legal_id VARCHAR(120) NULL,
    country_code CHAR(2) NULL,
    region VARCHAR(120) NULL,
    title VARCHAR(180) NOT NULL,
    description TEXT NULL,
    objectives TEXT NULL,
    deliverables TEXT NULL,
    required_profiles TEXT NULL,
    man_days INT UNSIGNED NOT NULL,
    visibility VARCHAR(40) NOT NULL DEFAULT 'open',
    status VARCHAR(40) NOT NULL DEFAULT 'pending_email_verification',
    verification_token_hash CHAR(64) NOT NULL,
    verified_email_at TIMESTAMP NULL,
    consent_at TIMESTAMP NOT NULL,
    submitted_ip VARCHAR(45) NULL,
    user_agent TEXT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    INDEX sponsorship_visibility_index (visibility),
    INDEX sponsorship_status_index (status),
    INDEX sponsorship_email_created_index (contact_email, created_at),
    CONSTRAINT sponsorship_country_fk FOREIGN KEY (country_code) REFERENCES countries(code) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE cause_sponsorship_mission (
    cause_id BIGINT UNSIGNED NOT NULL,
    sponsorship_mission_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (cause_id, sponsorship_mission_id),
    CONSTRAINT csm_cause_fk FOREIGN KEY (cause_id) REFERENCES causes(id) ON DELETE CASCADE,
    CONSTRAINT csm_mission_fk FOREIGN KEY (sponsorship_mission_id) REFERENCES sponsorship_missions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE sponsor_slots (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    placement VARCHAR(80) NOT NULL,
    sponsor_name VARCHAR(180) NOT NULL,
    label VARCHAR(80) NOT NULL DEFAULT 'Partenariat',
    copy TEXT NOT NULL,
    target_url VARCHAR(255) NULL,
    starts_at TIMESTAMP NULL,
    ends_at TIMESTAMP NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    INDEX sponsor_slots_placement_index (placement),
    INDEX sponsor_slots_active_index (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
