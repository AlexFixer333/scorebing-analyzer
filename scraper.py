import requests
from config import API_URL, API_KEY
from datetime import datetime, timedelta
import json

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
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 429:
            print("Ошибка: превышен лимит запросов API")
            return []
            
        response.raise_for_status()
        data = response.json()
        print(f"Получен ответ от API: {len(data.get('response', []))} матчей")
        
        matches = []
        
        if data.get('response'):
            print(f"Обрабатываем {len(data['response'])} матчей...")
            for fixture in data['response']:
                teams = fixture.get('teams', {})
                
                # Извлекаем коэффициенты из bookmakers
                odds_1 = None
                odds_x = None
                odds_2 = None
                
                bookmakers = fixture.get('bookmakers', [])
                if bookmakers:
                    for bookmaker in bookmakers:
                        bets = bookmaker.get('bets', [])
                        for bet in bets:
                            if bet.get('name') == 'Match Winner' or bet.get('id') == 1:
                                values = bet.get('values', [])
                                for value in values:
                                    val = value.get('value', '')
                                    odd = value.get('odd')
                                    if val == 'Home' and odd:
                                        odds_1 = float(odd)
                                    elif val == 'Draw' and odd:
                                        odds_x = float(odd)
                                    elif val == 'Away' and odd:
                                        odds_2 = float(odd)
                
                # Добавляем матч только если есть все коэффициенты
                if odds_1 and odds_x and odds_2:
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
        
        print(f"Всего найдено валидных матчей: {len(matches)}")
        return matches
        
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        import traceback
        traceback.print_exc()
        return []
