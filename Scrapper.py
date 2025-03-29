
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrap_contacts(_filename):
    f = _filename

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
            text = p.text.strip()
            # print("текст = ", text )

            # Поиск адресов
            if "россия" in text.lower():
                address = re.search(
                    r'\s*(\d{6}),\s*([^,]+),\s*([^,]+),\s*(г\.\s*[^,]+),\s*([^,]+),\s*(ул\.\s*[^,]+),\s*((д\.\d+)|(\d+\s*([^,.]+)))\.',
                    text)
                # address = re.search(r'\s*\d{6},.*?\.', text)
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
    # print(json_data)

    with open(f, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return json_data

def scrap_graf_work(_filename, _url):
    f = _filename

    url = _url
    response = requests.get(url)
    response.raise_for_status()
    data =[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        element = soup.find('div', itemprop ='articleBody') #  нужно чтобы мы искали первую таблицу внутри центарльного жлемента
        # Проверяем, найден ли элемент
        if element:
            # Извлекаем все строки внутри этого элемента
            table_grf = element.find('table')                   # основная таблица
            tables = table_grf.find_all('table')                # вложенные таблицы в основную таблицу

            rows = table_grf.find_all('tr')
            # print(rows)
            # text = table_grf.getText().strip()
            address = None
            name = None
            shedule = []

            for row in table_grf.find_all('tr'):
                col =  row.find_all('td')
                # print(len(col))
                if len(col) == 1:
                    address = col[0].get_text(strip=True)
                    # print(address)
                    shedule = []
                    slv = []
                    vtc = 0
                elif len(col) == 6 or len(col) == 8:
                    name = col[0].get_text(strip=True)
                    # print(name)
                # здесь можно попробовать найти элемент таблиц в основном хтмл или список таблиц и пройтись по таблицам
                elif len(col) == 2:
                    if vtc == 0:
                        vtc+=1
                        data.append({
                            'address': address,
                            'name': name,
                            'shedule': shedule
                        })
            for r, table in enumerate(tables):
                tmp = []
                for rvt in table.find_all('tr'):
                    cvt = rvt.find_all('td')
                    if len(cvt) == 2:
                        day = cvt[0].get_text(strip=True)
                        time = cvt[1].get_text(strip=True)
                        tmp.append({'day': day, 'time': time})
                slv.append(tmp)

            for i in range(len(data)):
                data[i]['shedule']  = slv[i]
        else:
            print("Элемент  не найден .")
    else:
        print("Страница не загружена .")

    # Форматирование данных в JSON
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Сохранение в JSON
    with open(_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в", _filename)
    return json_data

def scrap_graf_work_ddp(_filename):
    f =_filename

    url = "https://clinica.chitgma.ru/otdelenie-konsultativnoj-pomoshchi-detyam"

    response = requests.get(url)
    response.raise_for_status()
    data =[]

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        element = soup.find('div', itemprop ='articleBody') #  нужно чтобы мы искали первую таблицу внутри центарльного жлемента
        # Проверяем, найден ли элемент
        if element:

            # Извлекаем все строки внутри этого элемента
            table_grf = element.find('table')                   # основная таблица
            tables = table_grf.find_all('table')                # вложенные таблицы в основную таблицу

            rows = table_grf.find_all('tr')
            address = None
            name = None
            shedule = []

            paragraphs = element.find_all('p')
            for p in paragraphs:
                text = p.text.strip()
                if "отделение" in text.lower():
                    name = text.replace(':',"")
                    # print(name)

            for row in table_grf.find_all('tr'):
                col =  row.find_all('td')
                # print(len(col))
                if len(col) == 1:
                    address = col[0].get_text(strip=True)
                    # print(address)
                    shedule = []
                    slv = []
                    vtc = 0
                elif len(col) == 2:
                    if vtc == 0:
                        vtc+=1
                        data.append({
                            'address': address,
                            'name': name,
                            'shedule': shedule
                        })
            for r, table in enumerate(tables):
                tmp = []
                for rvt in table.find_all('tr'):
                    cvt = rvt.find_all('td')
                    if len(cvt) == 2:
                        day = cvt[0].get_text(strip=True)
                        time = cvt[1].get_text(strip=True)
                        tmp.append({'day': day, 'time': time})
                slv.append(tmp)

            for i in range(len(data)):
                data[i]['shedule']  = slv[i]

        else:
            print("Элемент  не найден .")
    else:
        print("Страница не загружена .")

    # Форматирование данных в JSON
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Сохранение в JSON
    with open(_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в", _filename)

    return json_data

url_dp = "https://clinica.chitgma.ru/diagnosticheskaya-poliklinika"
url_lab = "https://clinica.chitgma.ru/kliniko-diagnosticheskaya-laboratoriya"

# scrap_contacts('contacts.json')
scrap_graf_work('grafics_dp.json',url_dp)
scrap_graf_work_ddp('grafics_ddp.json')
scrap_graf_work('grafic_lab.json', url_lab)




# для гига чата
# OGM2N2NjZjUtOTU5OS00MDhiLWE5NzktN2M0YjM1Mjg3YjZhOjcwNzU4ZWQ0LWQ2NzEtNGI4Mi1iYjViLTVmMmRjZWQ1OTAzMg==

# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_gigachat.chat_models import GigaChat
#
# giga = GigaChat(
#     # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
#     credentials="OGM2N2NjZjUtOTU5OS00MDhiLWE5NzktN2M0YjM1Mjg3YjZhOjcwNzU4ZWQ0LWQ2NzEtNGI4Mi1iYjViLTVmMmRjZWQ1OTAzMg==",
#     verify_ssl_certs=False,
# )
#
# messages = [
#     SystemMessage(
#         content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
#     )
# ]
#
# while(True):
#     user_input = input("Пользователь: ")
#     if user_input == "пока":
#       break
#     messages.append(HumanMessage(content=user_input))
#     res = giga.invoke(messages)
#     messages.append(res)
#     print("GigaChat: ", res.content)
#



# from PyPDF2 import PdfReader
# import re
#
# # Указываем путь к PDF-файлу
# file_path = 'your_pdf_file.pdf'
#
# # Открываем PDF-файл для чтения
# with open(file_path, 'rb') as file:
#     reader = PdfReader(file)
#
# # Получаем список страниц
# pages = reader.pages
#
# # Итерируем по каждой странице и извлекаем текст
# for page in pages:
#     text = page['/Contents'].decode('utf-8')
#     # Используем регулярное выражение для поиска нужной информации
#     matches = re.findall(r'\bВаша информация\b', text)
#     if matches:
#         print("Найдена нужная информация:", matches[0])
