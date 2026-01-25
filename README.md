# GitHub Streak Checker

Script Python pour suivre votre streak GitHub et lister tous vos depots.

## Fonctionnalites

- Affiche votre streak actuel (jours consecutifs d'activite)
- Calcule le nombre de jours depuis votre premiere contribution recente
- Genere un fichier Markdown avec la liste de tous vos depots incluant :
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
STREAK Punkyherisson
Streak actuel: 18 jours
Jours depuis le debut: 18 jours (depuis 2025-12-05)
Dernieres dates: ['2025-12-22', '2025-12-21', ...]
Parfait !

Fichier cree: repositories22122025.MD (45 depots)
```

## Fichier genere

Le script cree un fichier `repositoriesDDMMYYYY.MD` contenant :

```markdown
- [NomDuRepo](lien) - Description
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

## Limites

- L'API GitHub Events ne retourne que les 90 derniers evenements
- Sans token d'authentification, l'API est limitee a 60 requetes/heure
- Le nombre de commits est approximatif pour les gros depots

## Licence

MIT
