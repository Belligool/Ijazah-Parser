import pytesseract
import numpy as np
from typing import Tuple

def extract_text_from_image(binary_image: np.ndarray) -> Tuple[str, float]:
    custom_config = r'--oem 3 --psm 4'
    data = pytesseract.image_to_data(
        binary_image,
        output_type=pytesseract.Output.DICT,
        config=custom_config
    )
    text_parts = []
    confidences = []
    for i, word in enumerate(data['text']):
        if word.strip():
            text_parts.append(word)
            confidences.append(int(data['conf'][i]))
    ocr_text = " ".join(text_parts)
    avg_conf = (sum(confidences) / len(confidences)) / 100.0 if confidences else 0.0
    return ocr_text, avg_conf