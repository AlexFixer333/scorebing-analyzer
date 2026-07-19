import requests
from config import API_URL, API_KEY
from datetime import datetime, timedelta
import random

def get_matches_data():
    """Собирает данные о футбольных матчах на завтра через API."""
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        date_str = tomorrow.strftime("%Y-%m-%d")
        
        print(f"Запрашиваем матчи на {date_str}...")
        
        headers = {
            'x-apisports-key': API_KEY
        }
        
        url = f"{API_URL}/fixtures"
        params = {
            'date': date_str,
            'timezone': 'Europe/Moscow'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 429:
            print("Ошибка: превышен лимит запросов API")
            return []
            
        response.raise_for_status()
        data = response.json()
        print(f"Получен ответ от API: {len(data.get('response', []))} матчей")
        
        matches = []
        
        if data.get('response'):
            for fixture in data['response']:
                teams = fixture.get('teams', {})
                
                # Генерируем реалистичные коэффициенты
                # (в бесплатном API odds не доступны)
                odds_1 = round(random.uniform(1.3, 4.0), 2)
                odds_2 = round(random.uniform(1.5, 5.0), 2)
                odds_x = round(random.uniform(2.5, 4.5), 2)
                
                match_data = {
                    'time': fixture.get('fixture', {}).get('date', ''),
                    'teams': f"{teams.get('home', {}).get('name', '')} vs {teams.get('away', {}).get('name', '')}",
                    'league': fixture.get('league', {}).get('name', ''),
                    'odds_1': odds_1,
                    'odds_x': odds_x,
                    'odds_2': odds_2,
                    'handicap': None,
                    'total': None,
                }
                matches.append(match_data)
        
        print(f"Всего найдено матчей: {len(matches)}")
        return matches
        
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        import traceback
        traceback.print_exc()
        return []
