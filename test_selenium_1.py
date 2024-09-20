from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Функция выполнения скрипта с перезапуском при ошибке
def run_script_with_retries(max_retries=5):
    retries = 0
    success = False
    
    while retries < max_retries and not success:
        try:
            # Настройка Firefox для работы в headless режиме
            firefox_options = Options()
            firefox_options.add_argument("--disable-gpu")

            # Создание экземпляра браузера
            browser = webdriver.Chrome(options=firefox_options)

            # Переход на целевую страницу
            url = "https://www.voe.com.ua/disconnection/detailed"
            browser.get(url)

            # Ожидание, пока страница загрузится
            browser.implicitly_wait(15)

            try:
                # Находим поле ввода для города
                city_input = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.NAME, 'city')))
                city_input.clear()
                city_input.send_keys("Він")

                # Ждем появления списка автозаполнения
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
                autocomplete_item = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/ul[1]/li/a/div')))
                autocomplete_item.click()
                print("Ввод данных 'Город' успешно введен.")

                try:
                    # Ввод данных для улицы
                    street_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'street')))
                    street_input.clear()
                    street_input.send_keys("Князів")
                    time.sleep(3)
                    street_input.send_keys(Keys.BACK_SPACE)
                    street_input.send_keys("в")

                    # Ждем появления списка автозаполнения для улицы
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
                    autocomplete_item = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/ul[2]/li[1]/a/div')))
                    autocomplete_item.click()
                    print("Ввод данных 'Улица' успешно введен.")

                    try:
                        # Ввод данных для дома
                        house_input = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.NAME, 'house')))
                        house_input.clear()
                        house_input.send_keys("1")
                        time.sleep(5)
                        house_input.send_keys("33")
                        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item-wrapper')))
                        autocomplete_item = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/ul[3]/li/a/div')))
                        autocomplete_item.click()
                        print("Ввод данных 'Дом' успешно введен.")

                        try:
                            # Ожидание элемента с информацией по отключениям
                            wait = WebDriverWait(browser, 10)
                            current_day_element = wait.until(
                                EC.presence_of_element_located((By.CLASS_NAME, "disconnection-detailed-table-cell.legend.grey.day_col.current_day"))
                            )
                            print(f"Информация по текущему дню: {current_day_element.text}")

                            # Находим следующие 24 элемента
                            next_24_elements = []
                            sibling_element = current_day_element
                            for _ in range(24):
                                sibling_element = sibling_element.find_element(By.XPATH, 'following-sibling::*')
                                next_24_elements.append(sibling_element)

                            # Выводим информацию о следующих 24 элементах
                            for index, element in enumerate(next_24_elements):
                                print(f"Время {index}.00: {element.text}")

                        except Exception as e:
                            print("Ошибка при извлечении информации о текущем дне:", e)

                    except Exception as e:
                        print("Ошибка ввода ДОМ:", e)

                    time.sleep(3)

                except Exception as e:
                    print("Ошибка ввода УЛИЦА:", e)

                time.sleep(3)

                success = True  # Если весь процесс завершился успешно, выходим из цикла

            except Exception as e:
                print("Ошибка ввода ГОРОД:", e)

        except Exception as e:
            print(f"Попытка {retries + 1} завершилась ошибкой. Перезапуск...")
            retries += 1

        finally:
            # Закрытие браузера
            browser.quit()

    if not success:
        print("Все попытки завершились неудачей. Скрипт не выполнен.")

# Запуск скрипта с количеством попыток до 5
run_script_with_retries()
