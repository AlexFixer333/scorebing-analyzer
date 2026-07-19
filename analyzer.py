import pandas as pd
import re

def analyze_trends(matches):
    """Анализирует данные и выявляет статистические закономерности."""
    if not matches:
        return {"error": "Нет данных для анализа"}

    df = pd.DataFrame(matches)
    
    insights = {
        "total_matches_processed": len(df),
        "high_total_opportunities": [],  # Матчи с высоким ожидаемым тоталом
        "handicap_anomalies": []         # Матчи с четкими форами для дальнейшего ручного анализа
    }

    # Закономерность 1: Поиск матчей с высоким ожидаемым тоталом (>= 2.5)
    for _, row in df.iterrows():
        total_str = str(row.get('total', ''))
        numbers = re.findall(r'\d+\.\d+', total_str)
        if numbers:
            total_val = float(numbers[0])
            if total_val >= 2.5:
                insights["high_total_opportunities"].append({
                    "teams": row.get('teams'),
                    "expected_total": total_val,
                    "time": row.get('time'),
                    "odds": row.get('odds_1x2')
                })

    # Закономерность 2: Фильтрация матчей с выраженной форой (например, -1.5, +1.5)
    for _, row in df.iterrows():
        hc_str = str(row.get('handicap', ''))
        if '-' in hc_str or '+' in hc_str:
            insights["handicap_anomalies"].append({
                "teams": row.get('teams'),
                "handicap": hc_str,
                "time": row.get('time')
            })

    return insights