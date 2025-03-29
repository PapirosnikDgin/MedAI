# vk_bot.py

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from MedAI_logic import handle_message

# Функция для создания клавиатуры
def create_keyboard(buttons):
    keyboard = VkKeyboard(one_time=False)
    for i, row in enumerate(buttons):
        for button_text in row:
            keyboard.add_button(button_text, color=VkKeyboardColor.PRIMARY)
        if i < len(buttons) - 1:  # Добавляем новую строку, если это не последняя строка
            keyboard.add_line()
    return keyboard.get_keyboard()

# Обработчик команды /start (аналогично Telegram)
def start():
    response = (
        "Здесь Вы можете найти всю необходимую информацию о нашей поликлинике и предоставляемых ей услугах.\n\n"
        "📍 Пожалуйста, выберите в приведенном ниже меню раздел, который Вас заинтересовал:\n"
        "Мы всегда рады помочь! 😊"
    )
    KEYBOARD = [["🏨Контакты", "🖊Запись на прием"], 
                ["⏱️Часы работы специалистов"]]
    return response, create_keyboard(KEYBOARD)

# Запуск бота
def run_MedAI_vk_bot():
    # Авторизация через токен
    TOKEN = "vk1.a.zHGOkliZpN3QtHrCETu4u_3YD0vBEpfCtBvBKL834hoGigeSazcZYmZHVcCDJpVAWL74H--epIw1Xxcu1kx6OGUKNkDfIxNfgqN1mnyveVANBCO5vJkQ9UkrwlDsJ33oJQwJtKs-PtfDYG27P6f7hL2Ian1WpL_z6CATUi1emmMngDsMkRmi01Cq6ihhsVRuTeEBalJVdJoheF2URG__8w"  # Замените на ваш токен
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    print("ВК-бот запущен...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            user_message = event.text
            print(f"Получено сообщение от пользователя {user_id}: {user_message}")
            # Обработка первого сообщения или команды "Начать"
            if user_message.lower() in ["начать", "start"]:
                response, KEYBOARD = start()
                vk.messages.send(
                    user_id=user_id,
                    message=response,
                    random_id=0,
                    keyboard=KEYBOARD
                )

            # Обработка остальных сообщений
            else:
                response, buttons = handle_message(user_message)
                KEYBOARD = create_keyboard(buttons)
                vk.messages.send(
                    user_id=user_id,
                    message=response,
                    random_id=0,
                    keyboard=KEYBOARD
                )
