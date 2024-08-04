from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re

# Настройка Firefox для работы в headless режиме
firefox_options = Options()
firefox_options.add_argument("--headless")

# Создание экземпляра браузера Firefox с указанными опциями
browser = webdriver.Firefox(options=firefox_options)

# Переход на целевую страницу
browser.get('https://advanced.name/ru/freeproxy?page=1')

# Получение HTML-кода страницы
html = browser.page_source

# Используем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html, 'html.parser')

# Поиск всех строк таблицы с помощью BeautifulSoup
rows = soup.find_all("tr")

# Перебор найденных строк и поиск данных IP и порта
for row in rows:
    ip_element = str(row.find(attrs={"data-ip": True}))
    port_element = str(row.find(attrs={"data-port": True}))

    ip = re.findall(r"<td data-ip[^>]+[>](\d+[.]\d+[.]\d+[.]\d+)<\/td>", ip_element)
    port = re.findall(r"<td data-port[^>]+[>](\d+)<\/td>", port_element)
    
    try:    
        ip_1 = f"{ip[0]}:{port[0]}"
        print(ip_1)
    except:
        continue    
    with open('proxy_1.txt', 'a') as proxys:
        proxys.write(ip_1 + '\n')
    
# Закрытие браузера
browser.quit()
