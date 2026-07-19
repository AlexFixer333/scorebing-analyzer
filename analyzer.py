import pandas as pd
from datetime import datetime, timedelta
import re

def is_tomorrow_match(time_str):
    """Проверяет, относится ли матч к завтрашнему дню."""
    if not time_str:
        return False
    
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%d.%m")  # Формат зависит от сайта
    
    # Проверяем различные форматы даты
    if tomorrow_str in time_str:
        return True
    
    # Если в time_str только время (например, "18:00"), считаем что это завтра
    if re.match(r'^\d{1,2}:\d{2}$', time_str):
        return True
    
    return False

def analyze_trends(matches):
    """Анализирует данные и находит топ-5 матчей в каждой категории."""
    if not matches:
        return {"error": "Нет данных для анализа"}

    df = pd.DataFrame(matches)
    
    # Фильтруем только завтрашние матчи
    df['is_tomorrow'] = df['time'].apply(is_tomorrow_match)
    tomorrow_matches = df[df['is_tomorrow']].copy()
    
    print(f"Матчей на завтра: {len(tomorrow_matches)}")
    
    insights = {
        "total_matches_processed": len(matches),
        "tomorrow_matches": len(tomorrow_matches),
        "home_wins": [],      # Вероятная победа хозяев
        "away_wins": [],      # Вероятная победа гостей
        "total_over": [],     # Больше голов
        "total_under": [],    # Меньше голов
    }
    
    # 1. Победа хозяев (низкий коэффициент odds_1)
    home_wins_df = tomorrow_matches.dropna(subset=['odds_1']).sort_values('odds_1')
    for _, row in home_wins_df.head(5).iterrows():
        insights["home_wins"].append({
            "teams": row.get('teams'),
            "time": row.get('time'),
            "odds_home_win": row.get('odds_1'),
            "probability": round((1 / row.get('odds_1')) * 100, 1) if row.get('odds_1') else 0
        })
    
    # 2. Победа гостей (низкий коэффициент odds_2)
    away_wins_df = tomorrow_matches.dropna(subset=['odds_2']).sort_values('odds_2')
    for _, row in away_wins_df.head(5).iterrows():
        insights["away_wins"].append({
            "teams": row.get('teams'),
            "time": row.get('time'),
            "odds_away_win": row.get('odds_2'),
            "probability": round((1 / row.get('odds_2')) * 100, 1) if row.get('odds_2') else 0
        })
    
    # 3. Тотал больше (низкий коэффициент total_over = высокая вероятность)
    over_df = tomorrow_matches.dropna(subset=['total_over']).sort_values('total_over')
    for _, row in over_df.head(5).iterrows():
        insights["total_over"].append({
            "teams": row.get('teams'),
            "time": row.get('time'),
            "odds_over": row.get('total_over'),
            "probability": round((1 / row.get('total_over')) * 100, 1) if row.get('total_over') else 0
        })
    
    # 4. Тотал меньше (низкий коэффициент total_under = высокая вероятность)
    under_df = tomorrow_matches.dropna(subset=['total_under']).sort_values('total_under')
    for _, row in under_df.head(5).iterrows():
        insights["total_under"].append({
            "teams": row.get('teams'),
            "time": row.get('time'),
            "odds_under": row.get('total_under'),
            "probability": round((1 / row.get('total_under')) * 100, 1) if row.get('total_under') else 0
        })
    
    return insights
