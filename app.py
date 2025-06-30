# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
import requests
from PIL import Image
from io import BytesIO
from run_model import process_image  # Импорт функции для обработки изображения

class ContentItem(BaseModel):
    type: str
    image: Union[str, None] = None
    text: Union[str, None] = None

class Message(BaseModel):
    role: str
    content: List[ContentItem]

class RequestBody(BaseModel):
    messages: List[Message]

app = FastAPI()

@app.post("/process")
async def process(request: RequestBody):
    try:
        message = request.messages[0]

        image_url = None
        instruction = None

        for item in message.content:
            if item.type == 'image' and item.image:
                image_url = item.image
            if item.type == 'text' and item.text:
                instruction = item.text

        if not image_url or not instruction:
            raise HTTPException(status_code=400, detail="Не найдены поля image или text в сообщении.")

        # Убираем лишние пробелы/символы в начале и конце
        image_url = image_url.strip()

        # Эмулируем браузер, чтобы избежать блокировки
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Пытаемся скачать изображение
        resp = requests.get(image_url, headers=headers)
        resp.raise_for_status()

        img = Image.open(BytesIO(resp.content)).convert('RGB')

        # Передаём PIL-изображение и инструкцию в модель
        result = process_image(img, instruction)
        return {"result": result}

    except HTTPException:
        raise
    except Exception as e:
        # Если сервер всё ещё блокирует — можно попросить клиента прислать base64-картинку
        raise HTTPException(
            status_code=500,
            detail=(
                f"Ошибка при скачивании изображения: {e}. "
                "Попробуйте передавать картинку как строку base64 в JSON поле image."
            )
        )
