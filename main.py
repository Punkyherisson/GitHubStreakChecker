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
    
    # Récupérer TOUS les dépôts via l'API repos
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_response = requests.get(repos_url)
    all_repos = []
    
    if repos_response.status_code == 200:
        repos_data = repos_response.json()
        for repo in repos_data:
            all_repos.append({
                'name': repo['name'],
                'full_name': repo['full_name'],
                'description': repo.get('description', ''),
                'url': repo['html_url'],
                'created_at': repo['created_at'][:10],
                'updated_at': repo['updated_at'][:10]
            })
    
    # Créer le fichier des dépôts
    today_str = datetime.now().strftime("%d%m%Y")
    filename = f"repositories{today_str}.MD"
    
    with open(filename, 'w') as f:
        f.write(f"# Depots GitHub de {username}\n")
        f.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write(f"## Liste des depots ({len(all_repos)} depots)\n\n")
        for repo in sorted(all_repos, key=lambda x: x['name'].lower()):
            desc = f" - {repo['description']}" if repo['description'] else ""
            f.write(f"- [{repo['name']}]({repo['url']}){desc}\n")
            f.write(f"  - Cree: {repo['created_at']} | Mis a jour: {repo['updated_at']}\n")
    
    print(f"\nFichier cree: {filename} ({len(all_repos)} depots)")

check_streak_detaille("Punkyherisson")
