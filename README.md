# ONG Back

Backend Django du projet ONG.

## Prérequis

- [Python 3.13+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) (gestion des dépendances et de l'environnement)
- [PostgreSQL 14+](https://www.postgresql.org/)

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-depot>
cd ong_back
```

### 2. Installer les dépendances

```bash
uv sync
```

Cela crée le `.venv` et installe les dépendances figées dans `uv.lock`.

### 3. Configurer les variables d'environnement

Copier le modèle puis renseigner les vraies valeurs :

```bash
# Windows (PowerShell)
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Variables attendues (voir `.env.example`) :

| Variable      | Description                    | Défaut       |
| ------------- | ------------------------------ | ------------ |
| `DB_NAME`     | Nom de la base PostgreSQL      | `ong_back`   |
| `DB_USER`     | Utilisateur PostgreSQL         | `postgres`   |
| `DB_PASSWORD` | Mot de passe                   | *your_psw*   |
| `DB_HOST`     | Hôte de la base                | `localhost`  |
| `DB_PORT`     | Port                           | `5432`       |

> ⚠️ Le fichier `.env` contient des secrets et **ne doit jamais être commité** (il est ignoré par `.gitignore`). Seul `.env.example` est versionné.

### 4. Créer la base de données

Dans PostgreSQL (`psql` ou pgAdmin) :

```sql
CREATE DATABASE ong_back;
```

### 5. Appliquer les migrations

```bash
uv run python manage.py migrate
```

### 6. (Optionnel) Créer un super-utilisateur

```bash
uv run python manage.py createsuperuser
```

## Lancer le serveur de développement

```bash
uv run python manage.py runserver
```

L'application est disponible sur http://127.0.0.1:8000/.

## Commandes utiles

| Commande                                  | Description                          |
| ----------------------------------------- | ------------------------------------ |
| `uv run python manage.py migrate`         | Appliquer les migrations             |
| `uv run python manage.py makemigrations`  | Générer de nouvelles migrations      |
| `uv run python manage.py check`           | Vérifier la configuration du projet  |
| `uv run python manage.py createsuperuser` | Créer un compte administrateur       |

## Conventions d'équipe

- Ne jamais commiter de secrets (`.env`, clés, mots de passe).
- Ajouter toute nouvelle variable de configuration dans `.env.example`.
- Versionner `uv.lock` (versions figées) ; ne pas versionner `.venv/`.

Chaque branche suit le format **`prenom/nom-feature`** :

- `prenom` : votre prénom en minuscules, sans accent
- `nom-feature` : description courte de la fonctionnalité, en minuscules,
  mots séparés par des tirets (`-`)
