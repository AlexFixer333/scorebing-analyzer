import os
import json
from datetime import datetime
from scraper import get_matches_data
from analyzer import analyze_trends
from config import OUTPUT_DIR

def export_to_txt(insights, output_file):
    """Экспортирует аналитику в читаемый TXT формат."""
    txt_file = output_file.replace('.json', '.txt')
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("SCOREBING ANALYTICAL REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Всего матчей обработано: {insights.get('total_matches_processed', 0)}\n\n")
        
        f.write("-" * 60 + "\n")
        f.write("МАТЧИ С ВЫСОКИМ ТОТАЛОМ (>= 2.5)\n")
        f.write("-" * 60 + "\n")
        for i, match in enumerate(insights.get('high_total_opportunities', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"    Время: {match.get('time', 'N/A')}\n")
            f.write(f"    Ожидаемый тотал: {match.get('expected_total', 'N/A')}\n")
            f.write(f"    Коэффициенты: {match.get('odds', 'N/A')}\n")
        
        f.write("\n" + "-" * 60 + "\n")
        f.write("МАТЧИ С ФОРАМИ\n")
        f.write("-" * 60 + "\n")
        for i, match in enumerate(insights.get('handicap_anomalies', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"    Время: {match.get('time', 'N/A')}\n")
            f.write(f"    Фора: {match.get('handicap', 'N/A')}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("Конец отчета\n")
    
    return txt_file

def main():
    print("Запуск Scorebing Analytical Tool...")
    
    # 1. Сбор данных
    print("Сбор данных с сайта...")
    matches = get_matches_data()
    print(f"Найдено {len(matches)} валидных записей о матчах.")
    
    # 2. Анализ данных
    print("Анализ закономерностей...")
    insights = analyze_trends(matches)
    
    # 3. Экспорт результатов
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = os.path.join(OUTPUT_DIR, f"analytical_report_{timestamp}.json")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(insights, f, ensure_ascii=False, indent=4)
        
    print(f"JSON отчет сохранен в: {json_file}")
    
    # 4. Экспорт в TXT
    txt_file = export_to_txt(insights, json_file)
    print(f"TXT отчет сохранен в: {txt_file}")
    
    # Демонстрация результатов
    print("\nТоп-3 возможности с высоким тоталом:")
    for opp in insights.get("high_total_opportunities", [])[:3]:
        print(f"   {opp['teams']} | Тотал: {opp['expected_total']} | Время: {opp['time']}")

if __name__ == "__main__":
    main()
