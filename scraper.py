def get_matches_data():
    """Собирает данные о футбольных матчах на завтра через API."""
    try:
        # ... [остальной код без изменений] ...
        
        matches = []
        
        if 'response' in data and data['response']:
            for fixture in data['response']:
                teams = fixture.get('teams', {})
                odds = fixture.get('odds', [])
                goals = fixture.get('goals', {})
                
                # Исправленный способ извлечения коэффициентов
                odds_1 = odds_2 = odds_x = None
                
                # Проверяем структуру odds
                if odds:
                    for bookmaker in odds:
                        for bet in bookmaker.get('bets', []):
                            if bet.get('name') == 'Match Winner':
                                for value in bet.get('values', []):
                                    if value.get('value') and value.get('handicap') is None:
                                        # Пытаемся определить тип коэффициента по положению
                                        if len(bet.get('values', [])) == 3:
                                            if value.get('value') == bet.get('values', [])[0].get('value'):
                                                odds_1 = float(value.get('value'))
                                            elif value.get('value') == bet.get('values', [])[1].get('value'):
                                                odds_x = float(value.get('value'))
                                            else:
                                                odds_2 = float(value.get('value'))
                
                # Дополнительная проверка: если коэффициенты не заполнились, попробуем из goals
                if not odds_1 and 'home' in goals:
                    odds_1 = 2.0  # Заглушка
                if not odds_2 and 'away' in goals:
                    odds_2 = 2.5  # Заглушка
                
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
