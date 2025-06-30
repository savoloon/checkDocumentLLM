import base64
from io import BytesIO
from PIL import Image
import ollama

class ModelProcessor:
    def __init__(self, model_name: str = "llama3.2-vision:90b"):
        self.model_name = model_name
        self.client = ollama

    def generate_caption(self, image: Image.Image, instruction: str) -> str:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": instruction,
                "images": [img_str]  # только base64 без "data:..."
            }
        ]

        response = self.client.chat(model=self.model_name, messages=messages)
        return response.get("message", {}).get("content", "")