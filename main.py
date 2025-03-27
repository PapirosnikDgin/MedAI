from threading import Thread
from MedAI_telegram_connector import run_MedAI_telegram_bot
from MedAI_vk_connector import run_MedAI_vk_bot



if __name__ == "__main__":
    # Запуск Telegram-бота в отдельном потоке
    telegram_thread = Thread(target=run_MedAI_telegram_bot, args=())
    vk_thread = Thread(target=run_MedAI_vk_bot, args=())
    telegram_thread.start()
    vk_thread.start()

    print("Боты запущены!")
    telegram_thread.join()
    vk_thread.join()