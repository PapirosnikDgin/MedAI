import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from MedAI_logic import handle_message
from user_registration import (
    is_user_registered, get_main_keyboard,
    get_consent_message, get_consent_denied_message, get_welcome_message, register_user, validate_name, validate_phone,
    CONSENT_KEYBOARD
)

# Состояния регистрации
REGISTRATION_STATES = {}

def create_keyboard(buttons):
    keyboard = VkKeyboard(one_time=False)
    for i, row in enumerate(buttons):
        for button_text in row:
            keyboard.add_button(button_text, color=VkKeyboardColor.PRIMARY)
        if i < len(buttons) - 1:
            keyboard.add_line()
    return keyboard.get_keyboard()

def start(user_id):
    if is_user_registered(user_id):
        response = (
            "Вы уже зарегистрированы! 😊\n\n"
            "Здесь Вы можете найти всю необходимую информацию о нашей поликлинике и предоставляемых ей услугах.\n\n"
            "📍Пожалуйста, выберите в приведенном ниже меню раздел, который Вас заинтересовал:"
        )
        return response, create_keyboard(get_main_keyboard())
    else:
        REGISTRATION_STATES[user_id] = {"step": "name"}
        return "Добро пожаловать! 🌟\n\nПожалуйста, введите ваше имя.", None

def run_MedAI_vk_bot():
    TOKEN = "vk1.a.zHGOkliZpN3QtHrCETu4u_3YD0vBEpfCtBvBKL834hoGigeSazcZYmZHVcCDJpVAWL74H--epIw1Xxcu1kx6OGUKNkDfIxNfgqN1mnyveVANBCO5vJkQ9UkrwlDsJ33oJQwJtKs-PtfDYG27P6f7hL2Ian1WpL_z6CATUi1emmMngDsMkRmi01Cq6ihhsVRuTeEBalJVdJoheF2URG__8w"
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    print("ВК-бот запущен...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            user_message = event.text
            
            # Обработка регистрации
            if user_id in REGISTRATION_STATES:
                state = REGISTRATION_STATES[user_id]
                
                if state["step"] == "name":
                    is_valid, error_message = validate_name(user_message)
                    if not is_valid:
                        vk.messages.send(
                            user_id=user_id,
                            message=error_message,
                            random_id=0
                        )
                        continue
                    
                    state["name"] = user_message
                    state["step"] = "phone"
                    vk.messages.send(
                        user_id=user_id,
                        message=f"Спасибо, {user_message}! Теперь введите ваш номер телефона.",
                        random_id=0
                    )
                    continue

                elif state["step"] == "phone":
                    is_valid, error_message = validate_phone(user_message)
                    if not is_valid:
                        vk.messages.send(
                            user_id=user_id,
                            message=error_message,
                            random_id=0
                        )
                        continue
                    
                    state["phone"] = user_message
                    state["step"] = "consent"
                    vk.messages.send(
                        user_id=user_id,
                        message=get_consent_message(state["name"]),
                        random_id=0,
                        keyboard=create_keyboard(CONSENT_KEYBOARD)
                    )
                    continue
                
                elif state["step"] == "consent":
                    if "да" in user_message.lower():
                        register_user(user_id, state["name"], state["phone"])
                        vk.messages.send(
                            user_id=user_id,
                            message=get_welcome_message(),
                            random_id=0,
                            keyboard=create_keyboard(get_main_keyboard())
                        )
                    else:
                        vk.messages.send(
                            user_id=user_id,
                            message=get_consent_denied_message(),
                            random_id=0,
                            keyboard=create_keyboard(get_main_keyboard())
                        )
                    del REGISTRATION_STATES[user_id]
                    continue
            
            # Обработка команды "Начать"
            if user_message.lower() in ["начать", "start"]:
                response, keyboard = start(user_id)
                vk.messages.send(
                    user_id=user_id,
                    message=response,
                    random_id=0,
                    keyboard=keyboard
                )
                continue
            
            # Обработка обычных сообщений
            response, buttons = handle_message(user_message, user_id)
            vk.messages.send(
                user_id=user_id,
                message=response,
                random_id=0,
                keyboard=create_keyboard(buttons)
            )