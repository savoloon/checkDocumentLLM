from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch

# одноразовая загрузка модели и процессора
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True,
    offload_folder="offload"
)
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

def process_images(images, instruction, max_new_tokens=128):
    """
    Возвращает список ответов: по одному описанию на каждое изображение.
    """
    results = []
    for img in images:
        messages = [{
            "role": "user",
            "content": [
                {"type": "image", "image": img},
                {"type": "text",  "text": instruction}
            ]
        }]
        # строим текстовую часть и визуальные токены
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        img_inputs, _ = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=img_inputs,
            padding=True,
            return_tensors="pt"
        ).to("cuda")
        # генерируем
        gen_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
        trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, gen_ids)]
        decoded = processor.batch_decode(trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        results.append(decoded[0])
    return results