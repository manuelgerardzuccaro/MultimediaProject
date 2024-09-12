import cv2
import numpy as np
from scipy.signal import wiener

def median_filter(image, ksize):

    if ksize < 1:
        ksize = 1

    # ksize deve essere un numero dispari
    if ksize % 2 == 0:
        ksize += 1  # Se ksize è pari, lo trasformiamo in un numero dispari

    # Applica il filtro mediano
    return cv2.medianBlur(image, ksize)

def mean_filter(image, kernel_size=3):

    if kernel_size < 1:
        kernel_size = 3  # Dimensione di default

    # Crea un kernel di dimensione kernel_size x kernel_size
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)

    # Applica il filtro di media aritmetica
    return cv2.filter2D(image, -1, kernel)

# Aggiungere qui gli altri filtri...
