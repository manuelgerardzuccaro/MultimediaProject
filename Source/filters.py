import cv2
import numpy as np


def median_filter(image, ksize):
    if ksize < 1:
        ksize = 1

    # ksize deve essere dispari
    if ksize % 2 == 0:
        ksize += 1

    return cv2.medianBlur(image, ksize)


def mean_filter(image, kernel_size=3):
    if kernel_size < 1:
        kernel_size = 3  # Dimensione di default

    # kernel_size x kernel_size
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)

    return cv2.filter2D(image, -1, kernel)


# altri filtri...