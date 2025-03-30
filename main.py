from threading import Thread
from MedAI_telegram_connector import run_MedAI_telegram_bot
from MedAI_vk_connector import run_MedAI_vk_bot
from Scrapper import run_Scrapper
import uvicorn
from api import app
from datetime import datetime

import time
import schedule

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_scrapper():
    scrapper_thread = Thread(target=run_Scrapper)
    scrapper_thread.start()
    scrapper_thread.join()

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Задержка для снижения нагрузки на процессор

if __name__ == "__main__":
    # Запуск FastAPI в отдельном потоке
    api_thread = Thread(target=run_fastapi)
    api_thread.start()

    # Запуск Telegram и VK ботов в отдельных потоках
    telegram_thread = Thread(target=run_MedAI_telegram_bot)
    vk_thread = Thread(target=run_MedAI_vk_bot)
    telegram_thread.start()
    vk_thread.start()

    run_scrapper()
    # Запланировать выполнение скрипта каждый день в 8:00
    schedule.every().day.at("08:00").do(run_scrapper)
    # Запуск проверщика расписания в отдельном потоке
    schedule_thread = Thread(target=schedule_checker)
    schedule_thread.start()

    print("API и боты запущены!")
    telegram_thread.join()
    vk_thread.join()
    api_thread.join()
    schedule_thread.join()



