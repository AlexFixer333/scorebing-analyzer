import requests
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS
from datetime import datetime, timedelta

def get_matches_data():
    """Собирает данные о матчах с сайта."""
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        matches = []
        # Ищем все строки с матчами (нужно адаптировать под реальную структуру сайта)
        rows = soup.find_all('tr', class_=lambda x: x and 'match' in x.lower())
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 8:  # Убедитесь, что достаточно колонок
                try:
                    # Извлекаем время матча
                    time_text = cols[0].get_text(strip=True)
                    
                    # Извлекаем команды
                    teams_text = cols[2].get_text(strip=True) if len(cols) > 2 else ""
                    
                    # Извлекаем коэффициенты (адаптируйте индексы под реальную структуру)
                    odds_1 = cols[3].get_text(strip=True) if len(cols) > 3 else ""
                    odds_x = cols[4].get_text(strip=True) if len(cols) > 4 else ""
                    odds_2 = cols[5].get_text(strip=True) if len(cols) > 5 else ""
                    total_over = cols[6].get_text(strip=True) if len(cols) > 6 else ""
                    total_under = cols[7].get_text(strip=True) if len(cols) > 7 else ""
                    
                    # Парсим коэффициенты (убираем нечисловые символы)
                    def parse_odds(odds_str):
                        if not odds_str:
                            return None
                        # Удаляем все кроме цифр и точки
                        clean = ''.join(c for c in odds_str if c.isdigit() or c == '.')
                        return float(clean) if clean else None
                    
                    match_data = {
                        'time': time_text,
                        'teams': teams_text,
                        'odds_1': parse_odds(odds_1),  # Победа хозяев
                        'odds_x': parse_odds(odds_x),  # Ничья
                        'odds_2': parse_odds(odds_2),  # Победа гостей
                        'total_over': parse_odds(total_over),  # Тотал больше
                        'total_under': parse_odds(total_under),  # Тотал меньше
                    }
                    
                    # Добавляем только если есть хотя бы команды и время
                    if match_data['teams'] and match_data['time']:
                        matches.append(match_data)
                        
                except (ValueError, IndexError) as e:
                    continue  # Пропускаем проблемные строки
                    
        print(f"Всего найдено матчей: {len(matches)}")
        return matches
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return []
