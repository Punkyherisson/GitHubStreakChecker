import requests
from datetime import datetime, timedelta

def check_streak_detaille(username):
    url = f"https://api.github.com/users/{username}/events/public"
    r = requests.get(url)
    
    if r.status_code != 200:
        print(f"Erreur: impossible de récupérer les données pour {username}")
        return
    
    events = r.json()
    
    if not events:
        print(f"Aucun événement public trouvé pour {username}")
        return
    
    # Récupérer les dates uniques
    dates = []
    repos = set()
    
    for event in events:
        date = event['created_at'][:10]  # YYYY-MM-DD
        if date not in dates:
            dates.append(date)
        
        # Récupérer le nom du dépôt
        repo = event.get('repo', {}).get('name', '')
        if repo:
            repos.add(repo)
    
    # Trier les dates
    dates.sort(reverse=True)
    
    # Calculer le streak actuel
    streak = 1
    for i in range(1, len(dates)):
        prev_date = datetime.strptime(dates[i-1], '%Y-%m-%d').date()
        curr_date = datetime.strptime(dates[i], '%Y-%m-%d').date()
        if (prev_date - curr_date).days == 1:
            streak += 1
        else:
            break
    
    # Calculer le nombre de jours depuis le début (première date dans les événements)
    first_date = datetime.strptime(min(dates), '%Y-%m-%d').date()
    today = datetime.now().date()
    days_since_start = (today - first_date).days + 1
    
    print(f"STREAK {username}")
    print(f"Streak actuel: {streak} jours")
    print(f"Jours depuis le debut: {days_since_start} jours (depuis {min(dates)})")
    print(f"Dernieres dates: {dates[:10]}")
    print("Parfait !")
    
    # Créer le fichier des dépôts
    today_str = datetime.now().strftime("%d%m%Y")
    filename = f"repositories{today_str}.MD"
    
    with open(filename, 'w') as f:
        f.write(f"# Depots GitHub de {username}\n")
        f.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write(f"## Liste des depots ({len(repos)} depots)\n\n")
        for repo in sorted(repos):
            f.write(f"- {repo}\n")
    
    print(f"\nFichier cree: {filename} ({len(repos)} depots)")

check_streak_detaille("Punkyherisson")
