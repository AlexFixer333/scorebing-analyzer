def main():
    print("Запуск Scorebing Analytical Tool...")
    
    # Создаем папку для данных
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Папка {OUTPUT_DIR} создана/проверена")

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
        f.write("=" * 70 + "\n")
        f.write("SCOREBING ANALYTICAL REPORT - МАТЧИ НА ЗАВТРА\n")
        f.write("=" * 70 + "\n")
        f.write(f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write(f"Всего матчей проанализировано: {insights.get('total_matches_processed', 0)}\n")
        f.write(f"Матчей на завтра: {insights.get('tomorrow_matches', 0)}\n")
        f.write("=" * 70 + "\n\n")
        
        # 1. Победа хозяев
        f.write("-" * 70 + "\n")
        f.write("🏆 ТОП-5: НАИБОЛЕЕ ВЕРОЯТНА ПОБЕДА ХОЗЯЕВ (П1)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('home_wins', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Коэффициент: {match.get('odds_home_win', 'N/A')}\n")
            f.write(f"   Вероятность: {match.get('probability', 0)}%\n")
        
        # 2. Победа гостей
        f.write("\n" + "-" * 70 + "\n")
        f.write("✈️ ТОП-5: НАИБОЛЕЕ ВЕРОЯТНА ПОБЕДА ГОСТЕЙ (П2)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('away_wins', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Коэффициент: {match.get('odds_away_win', 'N/A')}\n")
            f.write(f"   Вероятность: {match.get('probability', 0)}%\n")
        
        # 3. Тотал больше
        f.write("\n" + "-" * 70 + "\n")
        f.write("⚽ ТОП-5: НАИБОЛЬШЕЕ КОЛИЧЕСТВО ГОЛОВ (ТОТАЛ БОЛЬШЕ)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('total_over', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Коэффициент: {match.get('odds_over', 'N/A')}\n")
            f.write(f"   Вероятность: {match.get('probability', 0)}%\n")
        
        # 4. Тотал меньше
        f.write("\n" + "-" * 70 + "\n")
        f.write("️ ТОП-5: НАИМЕНЬШЕЕ КОЛИЧЕСТВО ГОЛОВ (ТОТАЛ МЕНЬШЕ)\n")
        f.write("-" * 70 + "\n")
        for i, match in enumerate(insights.get('total_under', []), 1):
            f.write(f"\n{i}. {match.get('teams', 'N/A')}\n")
            f.write(f"   Время: {match.get('time', 'N/A')}\n")
            f.write(f"   Коэффициент: {match.get('odds_under', 'N/A')}\n")
            f.write(f"   Вероятность: {match.get('probability', 0)}%\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("Конец отчета\n")
        f.write("=" * 70 + "\n")
    
    return txt_file

def main():
    print("Запуск Scorebing Analytical Tool...")
    print("Анализ матчей на завтра...\n")
    
    # 1. Сбор данных
    print("Сбор данных с сайта...")
    matches = get_matches_data()
    print(f"Найдено {len(matches)} матчей.\n")
    
    if len(matches) == 0:
        print("ОШИБКА: Не удалось собрать данные с сайта!")
        print("Возможно, изменилась структура сайта scorebing.com")
        return
    
    # 2. Анализ данных
    print("Анализ закономерностей...")
    insights = analyze_trends(matches)
    
    if "error" in insights:
        print(f"ОШИБКА: {insights['error']}")
        return
    
    print(f"Проанализировано матчей на завтра: {insights.get('tomorrow_matches', 0)}\n")
    
    # 3. Экспорт результатов
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = os.path.join(OUTPUT_DIR, f"analytical_report_{timestamp}.json")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(insights, f, ensure_ascii=False, indent=4)
        
    print(f"JSON отчет сохранен: {json_file}")
    
    # 4. Экспорт в TXT
    txt_file = export_to_txt(insights, json_file)
    print(f"TXT отчет сохранен: {txt_file}\n")
    
    # 5. Вывод краткой информации
    print("=" * 60)
    print("КРАТКИЕ РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    
    print("\n🏆 ТОП-1 Победа хозяев:")
    if insights.get('home_wins'):
        top = insights['home_wins'][0]
        print(f"   {top['teams']} (коэф: {top['odds_home_win']}, вер: {top['probability']}%)")
    
    print("\n✈️ ТОП-1 Победа гостей:")
    if insights.get('away_wins'):
        top = insights['away_wins'][0]
        print(f"   {top['teams']} (коэф: {top['odds_away_win']}, вер: {top['probability']}%)")
    
    print("\n⚽ ТОП-1 Тотал больше:")
    if insights.get('total_over'):
        top = insights['total_over'][0]
        print(f"   {top['teams']} (коэф: {top['odds_over']}, вер: {top['probability']}%)")
    
    print("\n🛡️ ТОП-1 Тотал меньше:")
    if insights.get('total_under'):
        top = insights['total_under'][0]
        print(f"   {top['teams']} (коэф: {top['odds_under']}, вер: {top['probability']}%)")
    
    print("\n✅ Анализ завершен!")

if __name__ == "__main__":
    main()
