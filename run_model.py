from model import ModelProcessor

processor = ModelProcessor()

def process_image(image, instruction: str) -> str:
    return processor.generate_caption(image, instruction)