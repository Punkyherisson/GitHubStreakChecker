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
    for event in events:
        date = event['created_at'][:10]  # YYYY-MM-DD
        if date not in dates:
            dates.append(date)
    
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
    
    print(f"STREAK {username}")
    print(f"Streak actuel: {streak} jours")
    print(f"Dernieres dates: {dates[:10]}")
    print("Parfait !")

check_streak_detaille("Punkyherisson")
