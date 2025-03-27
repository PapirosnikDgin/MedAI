
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time
import re
from bs4 import BeautifulSoup

"""
оформить функциями или классом Scrapper
"""

# text = """
# Фактический адрес:
# 1. 672038, Россия, Забайкальский край, г. Чита, Центральный административный район, ул. Новобульварная, д.163. Телефон регистратуры: 8 (3022) 71-51-00,
# """
#
# address = re.search( r'\d+\.\s*(\d{6}),\s*([^,]+),\s*([^,]+),\s*(г\.\s*[^,]+),\s*([^,]+),\s*(ул\.\s*[^,]+),\s*(д\.\d+)\.',text)
#
# print(address.group().strip())

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск в фоновом режиме
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL сайта
url = "https://clinica.chitgma.ru/contact"
# url = "https://clinica.chitgma.ru/grafik-raboty"
driver.get(url)

data = {
    'адрес': [],
    'телефон': [],
    'e-mail': []
}
try:
    #  берем элемент с данными с сайта
    element = driver.find_element(By.CSS_SELECTOR, "div[itemprop='articleBody']")

    # Извлекаем текст всех <p> внутри этого элемента
    paragraphs = element.find_elements(By.TAG_NAME, 'p')
    for p in paragraphs:
        # print(p.text)
        text =  p.text.strip()
        # print("текст = ", text )

        # Поиск адресов
        if "россия" in text.lower():
            address = re.search( r'\d+\.\s*(\d{6}),\s*([^,]+),\s*([^,]+),\s*(г\.\s*[^,]+),\s*([^,]+),\s*(ул\.\s*[^,]+),\s*(д\.\d+)\.',text)
            # address = re.search(r'\d+\.\s*\d{6},.*?\.', text)
            if address:
                data['адрес'].append(address.group().strip())

        # Поиск телефонов
        elif "телефон" in text.lower():
            phones = re.findall(r'\+?\d[\d\s()-]{4,}\d', text)
            data['телефон'].extend(phones)

        # Поиск email
        elif "e-mail" in text.lower():
            email = re.search(r'[\w\.-]+@[\w\.-]+', text)
            if email:
                data['e-mail'].append(email.group().strip())

except NoSuchElementException:
    print("Элемент нет.")

driver.quit()

# Форматирование данных в JSON
json_data = json.dumps(data, ensure_ascii=False, indent=4)
print(json_data)





#----------------------------------------------------------------------
# data = {'name': 'John', 'age': 30, 'city': 'New York'}

# with open('data.json', 'w') as file:
#     json.dump(data, file)







#----------------------------------------------------------------------------------------------------
# import requests
# from bs4 import BeautifulSoup
# import json
#
#
# url = "https://clinica.chitgma.ru/contact"
# response = requests.get(url)
#
# #response.raise_for_status()
# # print(response.text)
#
# # soup = BeautifulSoup(response.text, 'lxml')
#
# # Проверяем, успешен ли запрос
# if response.status_code == 200:
#     # Создаем объект BeautifulSoup
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     element = soup.find('div', itemprop ='articleBody')
#
#     # Проверяем, найден ли элемент
#     if element:
#         # Извлекаем все строки внутри этого элемента
#         spans = element.find_all('span')
#         # Выводим текст каждого
#         for s in spans:
#             print(s.get_text())
#     else:
#         print("Элемент  не найден .")
# else:
#     print(f"Ошибка при запросе: {response.status_code}")
