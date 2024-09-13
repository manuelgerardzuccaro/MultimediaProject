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


def geometric_mean_filter(image, kernel_size=3):
    if kernel_size < 1:
        kernel_size = 3

    pad_size = kernel_size // 2
    padded_image = cv2.copyMakeBorder(image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)

    filtered_image = np.zeros_like(image, dtype=np.float32)

    for i in range(pad_size, padded_image.shape[0] - pad_size):
        for j in range(pad_size, padded_image.shape[1] - pad_size):
            # Prendere il kernel della finestra
            window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
            product = np.prod(window)
            filtered_image[i - pad_size, j - pad_size] = product**(1.0 / (kernel_size * kernel_size))

    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image


def contra_harmonic_mean_filter(image, kernel_size=3, Q=1.0):
    if kernel_size < 1:
        kernel_size = 3

    pad_size = kernel_size // 2
    padded_image = cv2.copyMakeBorder(image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)

    filtered_image = np.zeros_like(image, dtype=np.float32)

    for i in range(pad_size, padded_image.shape[0] - pad_size):
        for j in range(pad_size, padded_image.shape[1] - pad_size):
            window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]

            num = np.sum(window**(Q + 1))
            den = np.sum(window**Q)

            if den != 0:
                filtered_image[i - pad_size, j - pad_size] = num / den
            else:
                filtered_image[i - pad_size, j - pad_size] = 0

    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image


def notch_filter(image, d0, u_k, v_k):
    # Trasformata di Fourier
    dft = np.fft.fft2(image)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = image.shape
    crow, ccol = rows // 2 , cols // 2

    # Costruire il filtro notch
    for u, v in zip(u_k, v_k):
        # Calcolare la distanza euclidea dal punto (u, v) e (-u, -v)
        for i in range(rows):
            for j in range(cols):
                duv = np.sqrt((i - (crow + u))**2 + (j - (ccol + v))**2)
                duv_neg = np.sqrt((i - (crow - u))**2 + (j - (ccol - v))**2)

                if duv < d0 or duv_neg < d0:
                    dft_shift[i, j] = 0  # Elimina queste frequenze

    # Inverti la trasformata di Fourier
    f_ishift = np.fft.ifftshift(dft_shift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    # Convertire a uint8
    return np.clip(img_back, 0, 255).astype(np.uint8)


# altri filtri...