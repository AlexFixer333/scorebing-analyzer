import requests
from config import API_URL, API_KEY
from datetime import datetime, timedelta

def get_matches_data():
    """Собирает данные о футбольных матчах на завтра через API."""
    try:
        # Завтрашняя дата
        tomorrow = datetime.now() + timedelta(days=1)
        date_str = tomorrow.strftime("%Y-%m-%d")
        
        print(f"Запрашиваем матчи на {date_str}...")
        
        headers = {
            'x-apisports-key': API_KEY
        }
        
        # Запрос к API (все матчи на завтра)
        url = f"{API_URL}/fixtures"
        params = {
            'date': date_str,
            'timezone': 'Europe/Moscow'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        matches = []
        
        if 'response' in data and data['response']:
            for fixture in data['response']:
                teams = fixture.get('teams', {})
                odds = fixture.get('odds', [])
                goals = fixture.get('goals', {})
                
                # Извлекаем коэффициенты (если есть)
                odds_1 = odds_2 = odds_x = None
                if odds:
                    for bookmaker in odds:
                        bets = bookmaker.get('bets', [])
                        for bet in bets:
                            if bet.get('name') == 'Match Winner':
                                values = bet.get('values', [])
                                if len(values) >= 3:
                                    odds_1 = float(values[0].get('value', 0))
                                    odds_x = float(values[1].get('value', 0))
                                    odds_2 = float(values[2].get('value', 0))
                
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
        return []
