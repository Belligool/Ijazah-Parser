import cv2
import numpy as np

def apply_adaptive_thresholding(gray_img: np.ndarray) -> np.ndarray:
    # blurred = cv2.bilateralFilter(gray_img, d=9, sigmaColor=75, sigmaSpace=75)
    blurred = gray_img
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=51, C=5)
    return binary