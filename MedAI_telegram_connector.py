from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from MedAI_logic import handle_message
from user_registration import (
    is_user_registered, register_user, get_main_keyboard,
    get_consent_message, get_consent_denied_message, get_welcome_message, load_users, validate_name, validate_phone,    
    CONSENT_KEYBOARD
)
import asyncio
import nest_asyncio
from callbacks import call_back, response_admin

nest_asyncio.apply()

# Состояния для ConversationHandler
NAME, PHONE, CONSENT = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    
    if is_user_registered(chat_id):
        reply_markup = ReplyKeyboardMarkup(get_main_keyboard(), resize_keyboard=True)
        await update.message.reply_text(
            "Вы уже зарегистрированы! 😊\n\n"
            "Здесь Вы можете найти всю необходимую информацию о нашей поликлинике и предоставляемых ей услугах.\n\n"
            "📍Пожалуйста, выберите в приведенном ниже меню раздел, который Вас заинтересовал:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    
    await update.message.reply_text("Добро пожаловать! 🌟\n\nПожалуйста, введите ваше имя.")
    return NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text
    is_valid, error_message = validate_name(name)
    
    if not is_valid:
        await update.message.reply_text(error_message)
        return NAME  # Остаёмся на этом же шаге
    
    context.user_data["name"] = name
    await update.message.reply_text(f"Спасибо, {name}! Теперь введите ваш номер телефона.")
    return PHONE

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone = update.message.text
    is_valid, error_message = validate_phone(phone)
    
    if not is_valid:
        await update.message.reply_text(error_message)
        return PHONE  # Остаёмся на этом же шаге
    
    context.user_data["phone"] = phone
    reply_markup = ReplyKeyboardMarkup(CONSENT_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        get_consent_message(context.user_data["name"]),
        reply_markup=reply_markup
    )
    return CONSENT

async def handle_consent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.lower()
    chat_id = update.message.chat_id
    
    if "да" in user_choice:
        register_user(chat_id, context.user_data["name"], context.user_data["phone"])
        reply_markup = ReplyKeyboardMarkup(get_main_keyboard(), resize_keyboard=True)
        await update.message.reply_text(
            get_welcome_message(),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        reply_markup = ReplyKeyboardMarkup(get_main_keyboard(), resize_keyboard=True)
        await update.message.reply_text(
            get_consent_denied_message(),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    context.user_data.clear()
    return ConversationHandler.END


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id
    
    # Проверка на административные команды
    if "///send" in user_message and chat_id == 6387671865:  # Ваш chat_id
        text = user_message.replace("///send", "")
        users = load_users()
        for user in users:
            try:
                await context.bot.send_message(chat_id=user["chat_id"], text=text)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user.get('name')}: {e}")
        return
    if "///RES_" in user_message and chat_id == 6387671865:
        text = user_message.replace("///RES_", "Ответ от администратора ID")
        id = user_message.replace("///RES_", "")[:10]
        await context.bot.send_message(chat_id=id, text=text)

    else:
        response, buttons = await handle_message(user_message, context,  chat_id)
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

def run_MedAI_telegram_bot() -> None:
    TOKEN = "7847641424:AAHIjA4LyDhYxkHpWpMdZJ_C6p5pwS4w4pw"
    application = Application.builder().token(TOKEN).build()
    
    # Настройка ConversationHandler для регистрации
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone)],
            CONSENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_consent)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.run_polling()