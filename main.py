import os
import json
from datetime import datetime
from scraper import get_matches_data
from analyzer import analyze_trends
from config import OUTPUT_DIR

def export_to_txt(insights, output_file):
    """Экспортирует аналитику в TXT формат."""
    txt_file = output_file.replace('.json', '.txt')
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("АНАЛИТИЧЕСКИЙ ОТЧЕТ - МАТЧИ НА ЗАВТРА\n")
        f.write("=" * 70 + "\n")
        f.write(f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write(f"Дата матчей: {insights.get('date', 'N/A')}\n")
        f.write(f"Всего матчей проанализировано: {insights.get('total_matches_processed', 0)}\n")
        f.write("=" * 70 + "\n\n")
        
        # 1. Победа хозяев
        f.write("-" * 70 + "\n")
        f.write("🏆 ТОП-5: НАИБОЛЕЕ ВЕРОЯТНА ПОБЕДА ХОЗЯЕВ (П1)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('home_wins', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Лига: {match.get('league', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Коэффициент: {match.get('odds_home_win', 'N/A')}\n")
            f.write(f"   Вероятность: {match.get('probability', 0)}%\n")
        
        # 2. Победа гостей
        f.write("\n" + "-" * 70 + "\n")
        f.write("✈️ ТОП-5: НАИБОЛЕЕ ВЕРОЯТНА ПОБЕДА ГОСТЕЙ (П2)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('away_wins', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Лига: {match.get('league', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Коэффициент: {match.get('odds_away_win', 'N/A')}\n")
            f.write(f"   Вероятность: {match.get('probability', 0)}%\n")
        
        # 3. Тотал больше
        f.write("\n" + "-" * 70 + "\n")
        f.write("⚽ ТОП-5: НАИБОЛЬШЕЕ КОЛИЧЕСТВО ГОЛОВ (ТОТАЛ БОЛЬШЕ)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('total_over', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Лига: {match.get('league', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Средний коэф: {match.get('avg_odds', 'N/A')}\n")
        
        # 4. Тотал меньше
        f.write("\n" + "-" * 70 + "\n")
        f.write("🛡️ ТОП-5: НАИМЕНЬШЕЕ КОЛИЧЕСТВО ГОЛОВ (ТОТАЛ МЕНЬШЕ)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('total_under', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Лига: {match.get('league', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Средний коэф: {match.get('avg_odds', 'N/A')}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("Конец отчета\n")
        f.write("=" * 70 + "\n")
    
    return txt_file

def main():
    print("Запуск аналитического инструмента...")
    print("Анализ матчей на завтра...\n")
    
    # Создаем папку
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Сбор данных
    print("Сбор данных через API...")
    matches = get_matches_data()
    print(f"Найдено {len(matches)} матчей.\n")
    
    if len(matches) == 0:
        print("ОШИБКА: Не удалось получить данные!")
        return
    
    # 2. Анализ
    print("Анализ данных...")
    insights = analyze_trends(matches)
    
    if "error" in insights:
        print(f"ОШИБКА: {insights['error']}")
        return
    
    print(f"Проанализировано матчей: {insights.get('total_matches_processed', 0)}\n")
    
    # 3. Экспорт
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = os.path.join(OUTPUT_DIR, f"analytical_report_{timestamp}.json")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(insights, f, ensure_ascii=False, indent=4)
        
    print(f"JSON сохранен: {json_file}")
    
    txt_file = export_to_txt(insights, json_file)
    print(f"TXT сохранен: {txt_file}\n")
    
    print("✅ Анализ завершен!")

if __name__ == "__main__":
    main()
