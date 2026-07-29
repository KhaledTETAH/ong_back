# ONG Back

Backend Django du projet ONG.

Cette branche couvre les pages 1 a 6 du cahier des charges avec Django REST
Framework, SimpleJWT et PostgreSQL.

## Pages couvertes

| Page | Endpoints principaux |
| --- | --- |
| Login | `/api/v1/auth/login/`, `/api/v1/auth/refresh/`, `/api/v1/auth/logout/`, `/api/v1/auth/me/`, `/api/v1/auth/register/candidate/`, `/api/v1/auth/register/organization/` |
| Portail public | `/api/v1/home/` |
| Missions | `/api/v1/offers/` |
| Annuaire ONG | `/api/v1/organizations/`, `/api/v1/organizations/<slug>/` |
| Mecenat de competences | `/api/v1/sponsorship-missions/`, tracking et verification par token |
| Detail offre | `/api/v1/offers/<slug>/`, `/api/v1/offers/<slug>/similar/`, apply/save/share |

## Prerequis

- Python 3.13+
- uv
- PostgreSQL 14+

## Installation

```bash
git clone <url-du-depot>
cd ong_back
uv sync
```

Copier le fichier d'environnement :

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Variables principales :

| Variable | Description |
| --- | --- |
| `DJANGO_SECRET_KEY` | Cle secrete Django |
| `DEBUG` | Active/desactive le mode debug |
| `ALLOWED_HOSTS` | Hotes autorises |
| `CORS_ALLOWED_ORIGINS` | URLs frontend autorisees |
| `DATABASE_URL` | URL PostgreSQL complete |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Parametres PostgreSQL separes |

## Base de donnees

Avec PostgreSQL local :

```sql
CREATE DATABASE ong_back;
```

Puis :

```bash
uv run python manage.py migrate
uv run python manage.py seed_demo
```

## Lancer le serveur

```bash
uv run python manage.py runserver
```

API locale :

```text
http://127.0.0.1:8000/api/v1/
```

## Tests

```bash
uv run python manage.py check
uv run python manage.py test apps.accounts apps.engagement
```

## Docker PostgreSQL

Le fichier `docker-compose.yaml` fournit un service PostgreSQL :

```bash
docker compose -f docker-compose.yaml up -d postgres
```

## Conventions d'equipe

- Ne jamais commiter `.env`, mots de passe ou secrets.
- Ajouter toute nouvelle variable dans `.env.example`.
- Versionner `uv.lock`.
- Ne pas versionner `.venv/`.
