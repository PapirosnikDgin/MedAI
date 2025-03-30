import json
import re
from typing import Dict, Any, Tuple

USERS_FILE = "users.json"
CONSENT_KEYBOARD = [["✅ ДА", "❌ НЕТ"]]

def load_users() -> list:
    try:
        with open(USERS_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users: list) -> None:
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def is_user_registered(chat_id: int) -> bool:
    users = load_users()
    return any(user.get("chat_id") == chat_id for user in users)

def validate_name(name: str) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "Имя не может быть пустым. Пожалуйста, введите ваше имя."
    if len(name.strip()) < 2:
        return False, "Имя слишком короткое. Пожалуйста, введите полное имя."
    return True, ""

def validate_phone(phone: str) -> Tuple[bool, str]:
    phone = phone.strip()
    if not phone:
        return False, "Номер телефона не может быть пустым. Пожалуйста, введите ваш номер телефона."
    
    # Проверка формата: +7XXXXXXXXXX или 8XXXXXXXXXX (X - цифра)
    pattern = r'^(\+7|8)\d{10}$'
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    if not re.match(pattern, phone):
        return False, "Номер телефона должен быть в формате: +7XXXXXXXXXX или 8XXXXXXXXXX (11 цифр)"
    
    return True, ""

def register_user(chat_id: int, name: str, phone: str) -> None:
    users = load_users()
    users.append({
        "chat_id": chat_id,
        "name": name.strip(),
        "phone": phone.strip(),
        "consent_given": True
    })
    save_users(users)

def get_main_keyboard():
    return [["🏨Контакты", "🖊Запись на прием", "Обратная связь"], 
            ["⏱️Часы работы специалистов", "🧪Исследования"]]

def get_consent_message(name: str) -> str:
    return (
        f"{name}, для продолжения работы с ботом необходимо ваше согласие "
        "на хранение, передачу и обработку персональных данных.\n\n"
        "Вы согласны?"
    )

def get_consent_denied_message() -> str:
    return (
        "Без вашего согласия на обработку персональных данных функционал бота будет ограничен.\n"
        "Вы можете воспользоваться основной информацией о поликлинике.\n"
        "Вы можете зарегистрироваться позже, используя команду /start."
    )

def get_welcome_message() -> str:
    return (
        "Спасибо! Ваши данные сохранены. 😊\n\n"
        "Теперь Вы можете воспользоваться нашими услугами. "
        "Выберите интересующий вас раздел:"
    )