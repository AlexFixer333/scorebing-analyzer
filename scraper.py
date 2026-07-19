import requests
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS

def get_matches_data():
    """Собирает данные о матчах с сайта."""
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        matches = []
        # Ищем строки таблиц (селекторы нужно будет уточнить под актуальные классы сайта, например, 'tr.match-row')
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 6:
                match_data = {
                    'time': cols[0].get_text(strip=True),
                    'score': cols[1].get_text(strip=True),
                    'teams': cols[2].get_text(strip=True), 
                    'odds_1x2': cols[3].get_text(strip=True),
                    'handicap': cols[4].get_text(strip=True),
                    'total': cols[5].get_text(strip=True)
                }
                # Простая валидация: строка должна содержать признак матча (например, "vs")
                if match_data['teams'] and 'vs' in match_data['teams'].lower():
                    matches.append(match_data)
                    
        return matches
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при запросе к сайту: {e}")
        return []