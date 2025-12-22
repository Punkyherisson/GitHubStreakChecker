import requests
from datetime import datetime, timedelta

def check_streak(username):
    """Vérifie les contributions GitHub d'un utilisateur"""
    
    # Utiliser l'API GitHub pour récupérer les événements publics
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    r = requests.get(url, headers=headers)
    
    if r.status_code != 200:
        print(f"Erreur: impossible de récupérer les données pour {username}")
        print(f"Status: {r.status_code}")
        return
    
    events = r.json()
    
    if not events:
        print(f"Aucun événement public trouvé pour {username}")
        return
    
    # Compter les jours avec des contributions
    contribution_dates = set()
    for event in events:
        date_str = event.get("created_at", "")[:10]  # Format: YYYY-MM-DD
        contribution_dates.add(date_str)
    
    print(f"Utilisateur: {username}")
    print(f"Nombre de jours avec activité (derniers événements): {len(contribution_dates)}")
    print(f"Dernière activité: {max(contribution_dates) if contribution_dates else 'Aucune'}")
    print(f"\nDates d'activité récentes:")
    for date in sorted(contribution_dates, reverse=True)[:5]:
        print(f"  - {date}")

check_streak("Punkyherisson")
