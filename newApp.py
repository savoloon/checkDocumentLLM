from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
import requests
from PIL import Image
from io import BytesIO
from newRun_model import process_images  # Импорт функции для обработки нескольких изображений

# Определяем модели запросов и контента
class ContentItem(BaseModel):
    type: str
    image: Union[str, None] = None
    text: Union[str, None] = None

class Message(BaseModel):
    role: str
    content: List[ContentItem]

class RequestBody(BaseModel):
    messages: List[Message]

# Инициализируем FastAPI-приложение
app = FastAPI()

@app.post("/process")
async def process(request: RequestBody):
    try:
        message = request.messages[0]

        image_urls = []  # список URL всех изображений
        instruction = None  # текстовая инструкция (одна)

        # Извлекаем из сообщения URL-ы изображений и инструкцию
        for item in message.content:
            if item.type == 'image' and item.image:
                image_urls.append(item.image.strip())  # убираем пробелы
            if item.type == 'text' and item.text:
                instruction = item.text.strip()

        # Проверяем наличие хотя бы одного изображения и инструкции
        if not image_urls:
            raise HTTPException(status_code=400, detail="Не найдены изображения в сообщении.")
        if not instruction:
            raise HTTPException(status_code=400, detail="Не найдена текстовая инструкция.")

        # Эмулируем браузер для корректного скачивания
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        images = []
        # Скачиваем все изображения
        for url in image_urls:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content)).convert('RGB')
            images.append(img)

        # Отправляем список PIL-изображений и инструкцию на обработку
        result = process_images(images, instruction)
        return {"result": result}

    except HTTPException:
        # Пробрасываем HTTP ошибки как есть
        raise
    except Exception as e:
        # Общая ошибка: предлагаем использовать base64 при проблемах со скачиванием
        raise HTTPException(
            status_code=500,
            detail=(
                f"Ошибка при скачивании или обработке изображения: {e}. "
                "Попробуйте передавать картинки как base64-строки в JSON-поле image."
            )
        )