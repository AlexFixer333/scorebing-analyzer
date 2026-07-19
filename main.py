import os
import json
from datetime import datetime
from scraper import get_matches_data
from analyzer import analyze_trends
from config import OUTPUT_DIR

def main():
    print("🚀 Запуск Scorebing Analytical Tool...")
    
    # 1. Сбор данных
    print("📥 Сбор данных с сайта...")
    matches = get_matches_data()
    print(f"✅ Найдено {len(matches)} валидных записей о матчах.")
    
    # 2. Анализ данных
    print("🔍 Анализ закономерностей...")
    insights = analyze_trends(matches)
    
    # 3. Экспорт результатов
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"analytical_report_{timestamp}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(insights, f, ensure_ascii=False, indent=4)
        
    print(f"💾 Отчет успешно сохранен в: {output_file}")
    
    # Демонстрация результатов
    print("\n📊 Топ-3 возможности с высоким тоталом:")
    for opp in insights.get("high_total_opportunities", [])[:3]:
        print(f"   ⚽ {opp['teams']} | Тотал: {opp['expected_total']} | Время: {opp['time']}")

if __name__ == "__main__":
    main()