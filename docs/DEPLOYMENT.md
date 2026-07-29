# Deployment guide

## Required services

- PHP-FPM 8.3 or newer;
- Nginx or Apache;
- MySQL 8 or compatible MariaDB;
- Redis;
- queue worker;
- scheduler;
- SMTP provider;
- private object storage for production uploads.

## Release procedure

```bash
composer install --no-dev --prefer-dist --optimize-autoloader
php artisan migrate --force
php artisan storage:link
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan queue:restart
```

Run the web server from the `public` directory only.

## Queue worker

The sponsorship verification email implements `ShouldQueue`.

Example Supervisor program:

```ini
[program:engagement-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/engagement/artisan queue:work redis --sleep=3 --tries=3 --timeout=90
autostart=true
autorestart=true
user=www-data
numprocs=2
redirect_stderr=true
stdout_logfile=/var/log/engagement-worker.log
stopwaitsecs=3600
```

## Scheduler

Add:

```cron
* * * * * cd /var/www/engagement && php artisan schedule:run >> /dev/null 2>&1
```

No scheduled command is mandatory for the six-page scope, but the scheduler should be available for future saved-search alerts and cleanup.

## Environment

Production minimum:

```dotenv
APP_ENV=production
APP_DEBUG=false
APP_URL=https://engagement.example
SESSION_SECURE_COOKIE=true
SESSION_SAME_SITE=lax
CACHE_STORE=redis
QUEUE_CONNECTION=redis
LOG_CHANNEL=stack
```

Set real MySQL, Redis, mail and OAuth credentials.

## Health checks

Laravel health endpoint:

```text
GET /up
```

Infrastructure should additionally monitor:

- database connection;
- Redis ping;
- queue age;
- disk/object-storage availability;
- SMTP delivery;
- HTTP latency and error rate.

## Database backups

Recommended:

- daily full backup;
- binary-log or point-in-time recovery;
- encrypted off-site copy;
- monthly restore test.

## Zero-downtime notes

- Run migrations before switching traffic.
- Avoid destructive migrations in the same release as application code requiring the new schema.
- Use `php artisan down --render=...` only when a migration cannot be made backward compatible.
