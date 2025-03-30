from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading
from MedAI_logic import handle_message
from MedAI_telegram_connector import run_MedAI_telegram_bot
from MedAI_vk_connector import run_MedAI_vk_bot

app = FastAPI()

class MessageRequest(BaseModel):
    text: str
    user_id: str  # Идентификатор пользователя в внешней системе

class MessageResponse(BaseModel):
    response: str
    buttons: list  # Кнопки для отображения в интерфейсе

@app.post("/qa/", response_model=MessageResponse)
async def handle_external_message(request: MessageRequest):
    """Обработка сообщений от внешней системы."""
    try:
        response, buttons = handle_message(request.text)
        return MessageResponse(response=response, buttons=buttons)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/start_bots/")
async def start_bots():
    """Запуск ботов в отдельных потоках."""
    try:
        telegram_thread = threading.Thread(target=run_MedAI_telegram_bot)
        vk_thread = threading.Thread(target=run_MedAI_vk_bot)
        telegram_thread.start()
        vk_thread.start()
        return {"status": "Боты запущены!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)