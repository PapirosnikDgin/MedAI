from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from MedAI_logic import handle_message
import asyncio
import nest_asyncio
import json

nest_asyncio.apply()
KEYBOARD = [["🏨Контакты", "🖊Запись на прием"], 
                ["⏱️Часы работы специалистов"]]
USERS_FILE = "users.json"
NAME, PHONE = range(2)


def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            content = file.read().strip()  # Читаем содержимое файла
            if not content:  # Если файл пустой
                return []
            return json.loads(content)  # Преобразуем JSON в Python-объект
    except FileNotFoundError:
        return []  # Если файл не существует, возвращаем пустой список
    except json.JSONDecodeError:
        print("Ошибка: Файл содержит некорректный JSON. Возвращаем пустой список.")
        return []  # В случае ошибки декодирования JSON, возвращаем пустой список
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    users = load_users()
    # Проверяем, зарегистрирован ли пользователь
    
    user_exists = any(user["chat_id"] == chat_id for user in users)

    if user_exists:
        reply_markup = ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
        await update.message.reply_text(
            "Вы уже зарегистрированы! 😊\n\n"
            "Здесь Вы можете найти всю необходимую информацию о нашей поликлинике и предоставляемых ей услугах.\n\n"
            "📍Пожалуйста, выберите в приведенном ниже меню раздел, который Вас заинтересовал:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return

    # Начинаем регистрацию
    context.user_data["step"] = "name"  # Устанавливаем первый шаг
    await update.message.reply_text("Добро пожаловать! 🌟\n\nПожалуйста, введите ваше имя.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user_message = update.message.text
    chat_id = update.message.chat_id
    if "step" not in context.user_data:
        if "///send" in user_message and chat_id == 6387671865:
            text = user_message.replace("///send", "")
            users = load_users()
            for user in users:
                try:
                    await context.bot.send_message(chat_id=user["chat_id"], text=text)
                except Exception as e:
                    name = user["name"]
                    print(f"Не удалось отправить сообщение пользователю {name}: {e}")
        else:
            response, KEYBOARD = handle_message(user_message)
            reply_markup = ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
            await update.message.reply_text(response,reply_markup=reply_markup, parse_mode="Markdown")

    # Обработка имени
    if context.user_data["step"] == "name":
        context.user_data["name"] = user_message
        context.user_data["step"] = "phone"  # Переходим к следующему шагу
        await update.message.reply_text(f"Спасибо, {user_message}! Теперь введите ваш номер телефона.")
        return

    # Обработка номера телефона
    if context.user_data["step"] == "phone":
        phone_number = user_message

        # Сохраняем данные
        users = load_users()
        users.append({
            "chat_id": chat_id,
            "name": context.user_data["name"],
            "phone": phone_number
        })
        save_users(users)

        # Очищаем данные регистрации
        context.user_data.clear()
        KEYBOARD = [["🏨Контакты", "🖊Запись на прием"], 
                ["⏱️Часы работы специалистов"]]
        reply_markup = ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
        
        await update.message.reply_text(
            "Спасибо! Ваши данные сохранены. 😊\n\n"
            "Теперь Вы можете воспользоваться нашими услугами. "
            "Выберите интересующий вас раздел:",
            parse_mode="Markdown", reply_markup=reply_markup
        )

def run_MedAI_telegram_bot() -> None:
    TOKEN = "7847641424:AAHIjA4LyDhYxkHpWpMdZJ_C6p5pwS4w4pw"
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

 
