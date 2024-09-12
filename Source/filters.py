import cv2
import numpy as np
from scipy.signal import wiener

def median_filter(image, ksize):
    return cv2.medianBlur(image, ksize)

def mean_filter(image):
    kernel = np.ones((3, 3), np.float32) / 9
    return cv2.filter2D(image, -1, kernel)

# Aggiungere qui gli altri filtri...
