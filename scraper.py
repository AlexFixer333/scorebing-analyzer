from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_matches_data():
    """Собирает данные о матчах на завтра с сайта scorimer.com."""
    try:
        # Настройка Chrome в headless режиме
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Запуск браузера
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("Открываем scorimer.com...")
        driver.get("https://scorimer.com/ru/")
        
        # Ждем загрузки страницы
        time.sleep(5)
        
        # Кликаем на вкладку "Tomorrow" (завтра)
        try:
            tomorrow_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Tomorrow') or contains(text(), 'Завтра')]"))
            )
            tomorrow_tab.click()
            print("Кликнули на вкладку 'Tomorrow'")
            time.sleep(3)  # Ждем загрузки матчей на завтра
        except Exception as e:
            print(f"Не удалось найти вкладку Tomorrow: {e}")
            print("Пробуем продолжить без фильтрации по дате...")
        
        # Ищем все строки с матчами
        matches = []
        
        # Пробуем разные селекторы для строк матчей
        try:
            # Вариант 1: ищем в таблице
            rows = driver.find_elements(By.CSS_SELECTOR, "table tr, .match-row, .event-row")
            
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 6:
                        time_text = cells[0].text.strip()
                        teams_text = cells[1].text.strip()
                        odds_text = cells[2].text.strip()  # Формат: "2.375 / 4.100 / 2.200"
                        handicap_text = cells[3].text.strip()
                        total_text = cells[4].text.strip()
                        
                        # Парсим коэффициенты
                        odds_parts = odds_text.split('/')
                        if len(odds_parts) >= 3:
                            odds_1 = float(odds_parts[0].strip())
                            odds_x = float(odds_parts[1].strip())
                            odds_2 = float(odds_parts[2].strip())
                        else:
                            odds_1 = odds_x = odds_2 = None
                        
                        match_data = {
                            'time': time_text,
                            'teams': teams_text,
                            'odds_1': odds_1,
                            'odds_x': odds_x,
                            'odds_2': odds_2,
                            'handicap': handicap_text,
                            'total': total_text,
                        }
                        
                        if match_data['teams']:
                            matches.append(match_data)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Ошибка при поиске строк: {e}")
        
        driver.quit()
        print(f"Всего найдено матчей: {len(matches)}")
        return matches
        
    except Exception as e:
        print(f"Ошибка при запуске браузера: {e}")
        return []
