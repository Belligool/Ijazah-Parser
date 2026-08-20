import cv2
import numpy as np

def remove_guilloche_background(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("No Image Exists/Could not read Image")
    b, g, r = cv2.split(img)
    return r

def keep_only_black_text(image_path: str):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 90])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    clean_canvas = np.full_like(img, 255)
    clean_canvas[mask == 255] = [0, 0, 0]
    return clean_canvas