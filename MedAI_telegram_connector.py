from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from MedAI_main import Get_main_info_CHIGMA


KEYBOARD = [["Информация"]]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "👋 **Здравствуйте!** \n"
        "Вы обратились в чат-бот поликлиники. Мы готовы ответить на ваши вопросы и помочь с:\n\n"
        "📋 *Записью к врачу*\n"
        "🗓️ *Расписанием работы специалистов*\n"
        "📄 *Необходимыми документами*\n"
        "🏥 *Услугами нашей клиники*\n\n"
        "📍 Я умею:\n"
        "• Предоставлять актуальную информацию об адресах наших клиник\n"
        "• Сообщать часы работы\n"
        "• Делиться контактами колл-центров\n\n"
        "(❗ _Позже добавлю дополнительные функции._)\n\n"
        "Пожалуйста, уточните ваш вопрос или просьбу. Для этого вы можете использовать навигацию в выпадающем меню.\n"
    "• Если не нашли свой вопрос, вы можете написать свой вопрос в свободной форме.\n\n"
    "Мы всегда рады помочь! 😊", reply_markup=reply_markup, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    if user_message == "Информация":
        response = (Get_main_info_CHIGMA())
    await update.message.reply_text(response, parse_mode="Markdown")

def main() -> None:
    TOKEN = "7847641424:AAHIjA4LyDhYxkHpWpMdZJ_C6p5pwS4w4pw"
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
 
