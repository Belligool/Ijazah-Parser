import numpy as np
import easyocr

print("Loading Deep Learning OCR Models...")
reader = easyocr.Reader(['id', 'en'], gpu=True)

def extract_text_from_image(image_array: np.ndarray) -> tuple[str, float]:
    results = reader.readtext(image_array, detail=1, paragraph=False)
    extracted_lines = []
    confidences = []
    
    for (bbox, text, prob) in results:
        extracted_lines.append(text)
        confidences.append(prob)
    full_text = "\n".join(extracted_lines)
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    return full_text, avg_confidence