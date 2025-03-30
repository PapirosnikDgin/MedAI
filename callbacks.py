async def call_back(bot, phone, name):
    text = f"ЗАКАЗ НА ОБРАТНЫЙ ЗВОНОК ОТ: {name} НОМЕР: {phone}"
    await bot.send_message(chat_id=6387671865, text=text)

async def response_admin(bot, id, phone, name, q):
    text = f"ЗАКАЗ НА ОТВЕТ ОТ {name} НОМЕР: {phone} ТЕКСТ СООБЩЕНИЯ: {q} ОТВЕТИТЬ ПОЛЬЗОВАТЕЛЮ МОЖНО КОМАНДОЙ ///RES_{id}"
    await bot.send_message(chat_id=6387671865, text=text)