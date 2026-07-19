import pandas as pd
from datetime import datetime

def analyze_trends(matches):
    """Анализирует данные и находит топ-5 матчей в каждой категории."""
    if not matches:
        return {"error": "Нет данных для анализа"}

    df = pd.DataFrame(matches)
    
    insights = {
        "total_matches_processed": len(matches),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "home_wins": [],
        "away_wins": [],
        "total_over": [],
        "total_under": [],
    }
    
    # 1. Победа хозяев (низкий коэффициент odds_1)
    home_wins_df = df.dropna(subset=['odds_1']).sort_values('odds_1')
    for _, row in home_wins_df.head(5).iterrows():
        insights["home_wins"].append({
            "teams": row.get('teams'),
            "league": row.get('league'),
            "time": row.get('time'),
            "odds_home_win": row.get('odds_1'),
            "probability": round((1 / row.get('odds_1')) * 100, 1) if row.get('odds_1') else 0
        })
    
    # 2. Победа гостей (низкий коэффициент odds_2)
    away_wins_df = df.dropna(subset=['odds_2']).sort_values('odds_2')
    for _, row in away_wins_df.head(5).iterrows():
        insights["away_wins"].append({
            "teams": row.get('teams'),
            "league": row.get('league'),
            "time": row.get('time'),
            "odds_away_win": row.get('odds_2'),
            "probability": round((1 / row.get('odds_2')) * 100, 1) if row.get('odds_2') else 0
        })
    
    # 3. Тотал больше (упрощенно - по среднему коэффициенту)
    # В реальном API можно запросить конкретные тоталы
    over_df = df.dropna(subset=['odds_1', 'odds_2']).copy()
    over_df['avg_odds'] = (over_df['odds_1'] + over_df['odds_2']) / 2
    over_df = over_df.sort_values('avg_odds')
    for _, row in over_df.head(5).iterrows():
        insights["total_over"].append({
            "teams": row.get('teams'),
            "league": row.get('league'),
            "time": row.get('time'),
            "avg_odds": round(row.get('avg_odds'), 2),
        })
    
    # 4. Тотал меньше
    under_df = over_df.tail(5)
    for _, row in under_df.iterrows():
        insights["total_under"].append({
            "teams": row.get('teams'),
            "league": row.get('league'),
            "time": row.get('time'),
            "avg_odds": round(row.get('avg_odds'), 2),
        })
    
    return insights
