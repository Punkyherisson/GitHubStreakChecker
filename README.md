# GitHub Streak Checker

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![GitHub API](https://img.shields.io/badge/GitHub-API%20v3-181717?logo=github)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Repos](https://img.shields.io/badge/Repos-Public%20%2B%20Priv%C3%A9s-orange)
![Made with](https://img.shields.io/badge/Made%20with-Replit-667881?logo=replit)

Script Python pour suivre votre streak GitHub et lister tous vos depots (publics et prives).

## Fonctionnalites

- Affiche votre streak actuel (jours consecutifs d'activite)
- Calcule le nombre de jours depuis votre premiere contribution
- Supporte les repos publics ET prives (avec token)
- Genere un fichier Markdown avec la liste de tous vos depots incluant :
  - Visibilite (public/prive)
  - Nombre de commits
  - Presence d'un README
  - Type de licence
  - Dates de creation et derniere mise a jour

## Utilisation

```bash
python3 main.py
```

## Exemple de sortie

```
Mode authentifie (repos publics + prives)

STREAK Punkyherisson
Streak actuel: 26 jours
Jours depuis le debut: 397 jours (depuis 2024-12-25)
Dernieres dates: ['2026-01-24', '2026-01-23', ...]
Parfait !

Recuperation des details pour 50 depots...
  [1/50] AbosUtilization (PRIVE)
  [2/50] Automation (public)
  ...

Fichier cree: repositories25012026.MD (50 depots)
```

## Fichier genere

Le script cree un fichier `repositoriesDDMMYYYY.MD` contenant :

```markdown
## Liste des depots (50 depots)
- Publics: 45
- Prives: 5

- [NomDuRepo](lien) [PRIVE] - Description
  - Commits: X | README: Oui/Non | Licence: MIT/Non
  - Cree: YYYY-MM-DD | Mis a jour: YYYY-MM-DD
```

## Configuration

Pour utiliser avec votre propre compte GitHub, modifiez la derniere ligne de `main.py` :

```python
check_streak_detaille("VotreNomUtilisateur")
```

## Dependances

- Python 3
- requests

## Installation

```bash
pip install requests
```

## Utilisation d'un Personal Access Token (PAT)

### Pourquoi utiliser un PAT ?

| Sans PAT | Avec PAT |
|----------|----------|
| 60 requetes/heure | 5000 requetes/heure |
| Repos publics uniquement | Repos publics + prives |
| Peut echouer avec beaucoup de repos | Stable et rapide |

### Faut-il en utiliser un ?

- **Non necessaire** si vous avez moins de 30 repos publics et executez le script occasionnellement
- **Recommande** si vous avez beaucoup de repos ou executez le script frequemment
- **Obligatoire** si vous voulez voir vos repos prives

### Comment creer un PAT

1. Allez sur [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Cliquez sur "Generate new token (classic)"
3. Donnez un nom (ex: "Streak Checker")
4. Selectionnez les permissions : `repo` (pour les repos prives) ou `public_repo` (repos publics uniquement)
5. Copiez le token genere

### Comment l'utiliser

Ajoutez votre token dans le code en modifiant les headers :

```python
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": "token VOTRE_TOKEN_ICI"
}
```

Ou utilisez une variable d'environnement (plus securise) :

```python
import os
token = os.environ.get("GITHUB_TOKEN")
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}"
}
```

> **Attention** : Ne commitez jamais votre token directement dans le code ! Utilisez des variables d'environnement ou un fichier `.env` ignore par git.

## Limites

- L'API GitHub Events ne retourne que les 90 derniers evenements
- Sans token d'authentification, l'API est limitee a 60 requetes/heure
- Le nombre de commits est approximatif pour les gros depots

## Licence

MIT
