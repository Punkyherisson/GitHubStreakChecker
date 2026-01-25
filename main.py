import requests
import os
import re
from datetime import datetime, timedelta

def check_streak_detaille(username):
    # Configuration du token pour acceder aux repos prives
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if token:
        headers["Authorization"] = f"token {token}"
        print("Mode authentifie (repos publics + prives)")
    else:
        print("Mode public uniquement (ajoutez GITHUB_TOKEN pour les repos prives)")
    
    print()
    
    # Récupérer les événements
    url = f"https://api.github.com/users/{username}/events/public"
    r = requests.get(url, headers=headers)
    
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
    
    # Récupérer TOUS les dépôts (publics + prives si authentifie)
    if token:
        # Avec token: utiliser /user/repos pour avoir les repos prives
        repos_url = "https://api.github.com/user/repos?per_page=100&affiliation=owner"
    else:
        # Sans token: repos publics uniquement
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    
    repos_response = requests.get(repos_url, headers=headers)
    all_repos = []
    
    if repos_response.status_code == 200:
        repos_data = repos_response.json()
        total = len(repos_data)
        print(f"\nRecuperation des details pour {total} depots...")
        
        for i, repo in enumerate(repos_data):
            # Récupérer le nombre de commits
            commits_url = f"https://api.github.com/repos/{repo['full_name']}/commits?per_page=1"
            commits_response = requests.get(commits_url, headers=headers)
            commit_count = 0
            if commits_response.status_code == 200:
                # Le nombre total est dans le header Link
                link_header = commits_response.headers.get('Link', '')
                if 'last' in link_header:
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        commit_count = int(match.group(1))
                else:
                    # Si pas de pagination, compter les commits retournés
                    commit_count = len(commits_response.json())
            
            # Vérifier si README existe
            readme_url = f"https://api.github.com/repos/{repo['full_name']}/readme"
            readme_response = requests.get(readme_url, headers=headers)
            has_readme = readme_response.status_code == 200
            
            # License depuis les données du repo
            license_info = repo.get('license')
            has_license = license_info is not None
            license_name = license_info.get('name', '') if license_info else ''
            
            # Visibilité (public ou privé)
            is_private = repo.get('private', False)
            
            all_repos.append({
                'name': repo['name'],
                'full_name': repo['full_name'],
                'description': repo.get('description', ''),
                'url': repo['html_url'],
                'created_at': repo['created_at'][:10],
                'updated_at': repo['updated_at'][:10],
                'commits': commit_count,
                'has_readme': has_readme,
                'has_license': has_license,
                'license_name': license_name,
                'is_private': is_private
            })
            
            visibility = "PRIVE" if is_private else "public"
            print(f"  [{i+1}/{total}] {repo['name']} ({visibility})")
    
    # Créer le fichier des dépôts
    today_str = datetime.now().strftime("%d%m%Y")
    filename = f"repositories{today_str}.MD"
    
    # Compter les repos publics et privés
    public_count = sum(1 for r in all_repos if not r['is_private'])
    private_count = sum(1 for r in all_repos if r['is_private'])
    
    with open(filename, 'w') as f:
        f.write(f"# Depots GitHub de {username}\n")
        f.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write(f"## Liste des depots ({len(all_repos)} depots)\n")
        f.write(f"- Publics: {public_count}\n")
        f.write(f"- Prives: {private_count}\n\n")
        
        for repo in sorted(all_repos, key=lambda x: x['name'].lower()):
            visibility = " [PRIVE]" if repo['is_private'] else ""
            desc = f" - {repo['description']}" if repo['description'] else ""
            f.write(f"- [{repo['name']}]({repo['url']}){visibility}{desc}\n")
            
            readme_status = "Oui" if repo['has_readme'] else "Non"
            license_status = repo['license_name'] if repo['has_license'] else "Non"
            
            f.write(f"  - Commits: {repo['commits']} | README: {readme_status} | Licence: {license_status}\n")
            f.write(f"  - Cree: {repo['created_at']} | Mis a jour: {repo['updated_at']}\n")
    
    print(f"\nFichier cree: {filename} ({len(all_repos)} depots)")

check_streak_detaille("Punkyherisson")
