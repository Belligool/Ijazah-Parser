import cv2
import numpy as np

def remove_guilloche_background(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("No Image Exists/Could not read Image")
    b, g, r = cv2.split(img)
    return r