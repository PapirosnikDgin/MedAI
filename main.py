from threading import Thread
from MedAI_telegram_connector import run_MedAI_telegram_bot
from MedAI_vk_connector import run_MedAI_vk_bot
import uvicorn
from api import app

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Запуск FastAPI в отдельном потоке
    api_thread = Thread(target=run_fastapi)
    api_thread.start()

    # Запуск Telegram и VK ботов в отдельных потоках
    telegram_thread = Thread(target=run_MedAI_telegram_bot)
    vk_thread = Thread(target=run_MedAI_vk_bot)
    telegram_thread.start()
    vk_thread.start()

    print("API и боты запущены!")
    telegram_thread.join()
    vk_thread.join()
    api_thread.join()