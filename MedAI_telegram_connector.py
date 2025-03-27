from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from MedAI_logic import handle_message
import asyncio
import nest_asyncio

nest_asyncio.apply()
KEYBOARD = [["Информация"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["state"] = "0"
    reply_markup = ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "Здесь Вы можете найти всю необходимую информацию о нашей поликлинике и предоставляемых ей услугах\n\n"
        "📍Пожалуйста, выберите в приведенном ниже меню раздел, которые Вас заинтересовал:\n"
    "Мы всегда рады помочь! 😊", reply_markup=reply_markup, parse_mode="Markdown")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    response, KEYBOARD = handle_message(user_message)
    reply_markup = ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(response,reply_markup=reply_markup, parse_mode="Markdown")

def run_MedAI_telegram_bot() -> None:
    TOKEN = "7847641424:AAHIjA4LyDhYxkHpWpMdZJ_C6p5pwS4w4pw"
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

 
