from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import os
from dotenv import load_dotenv

load_dotenv()

class GigaChatIntegration:
    def __init__(self):
        # Получаем credentials из переменных окружения (без хардкода)
        credentials = os.getenv("GIGACHAT_CREDENTIALS")
        if not credentials:
            raise ValueError("GIGACHAT_CREDENTIALS не установлен в .env файле")
            
        self.client = GigaChat(
            credentials=credentials,
            scope="GIGACHAT_API_PERS",
            verify_ssl_certs=False  # Только для тестов! В продакшене должно быть True
        )
        self.system_prompt = """
        Ты - виртуальный помощник поликлиники. Отвечай вежливо и профессионально.
        Если вопрос не связан с медициной или поликлиникой, вежливо сообщи, что не можешь помочь.
        Используй только предоставленную информацию о поликлинике.
        Контакты поликлиники:
        - Адрес: ул. Бабушкина, 44
        - Телефон: 8 (3022) 73-70-73
        - Email: diagnost_chita@mail.ru
        """
    
    def get_response(self, user_message):
        try:
            # Автоматическое управление сессией через контекстный менеджер
            with self.client as giga:
                chat = Chat(
                    messages=[
                        Messages(role=MessagesRole.SYSTEM, content=self.system_prompt),
                        Messages(role=MessagesRole.USER, content=user_message)
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                response = giga.chat(chat)
                return response.choices[0].message.content
                
        except Exception as e:
            print(f"Ошибка GigaChat: {e}")
            # Возвращаем стандартное сообщение об ошибке
            return "Извините, в данный момент я не могу обработать ваш запрос. Пожалуйста, попробуйте позже или обратитесь в регистратуру по телефону 8 (3022) 73-70-73."