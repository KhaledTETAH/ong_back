# Security design

## Authentication

- Browser sessions use Laravel's session guard and CSRF middleware.
- API clients use Sanctum bearer tokens.
- Tokens are hashed before database storage.
- Login is limited to five attempts per minute per email/IP.
- Session ID is regenerated after login.
- Logout invalidates the browser session or revokes the current API token.
- Passwords require at least 10 characters, mixed case and a number on registration/reset.

## Authorization

- Candidate actions require `auth:sanctum`, a candidate role and a dedicated rate limiter.
- Public organization data is restricted to active verified/Certified+ organizations.
- Draft, paused, closed and expired offers are not returned by public queries.
- Sensitive fields are omitted by API resources.

## Submission protection

The public skills-sponsorship form uses:

- strict server-side validation;
- a hidden honeypot field;
- five submissions per hour per IP;
- a random 64-character verification token;
- SHA-256 token storage;
- email confirmation before moderation;
- a random UUID for tracking.

Recommended production additions:

- Cloudflare Turnstile or hCaptcha;
- IP reputation/abuse service;
- email-domain risk checks;
- malware scanning for attachments;
- moderation queues and audit logs.

## Uploaded files

Private disk:

- organization verification documents;
- candidate CVs.

Production recommendations:

1. Store private files in S3-compatible object storage.
2. Use server-side encryption.
3. Generate short-lived signed download URLs.
4. Scan every upload before making it available.
5. Validate MIME content, not only extensions.
6. Keep access logs.

## Privacy

- Raw IP and user agent are not exposed through APIs.
- Offer share analytics store SHA-256 hashes only.
- Social provider access and refresh tokens use Laravel encrypted casts.
- Password-reset responses do not reveal whether an email exists.

## Production headers

The included Nginx config sets:

- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- a strict referrer policy;
- a restrictive permissions policy.

Add a tested Content Security Policy before production, especially because the prototype currently loads Google Fonts and Bootstrap from CDNs.

## Operational checklist

- Disable `APP_DEBUG`.
- Use HTTPS and `SESSION_SECURE_COOKIE=true`.
- Use a real secret manager.
- Rotate provider credentials and application keys.
- Restrict database and Redis network access.
- Back up MySQL and object storage.
- Monitor failed logins, sponsorship bursts and upload failures.
- Run dependency audits in CI.
- Keep Laravel, PHP and container images patched.
