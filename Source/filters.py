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
            filtered_image[i - pad_size, j - pad_size] = product ** (1.0 / (kernel_size * kernel_size))

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

            num = np.sum(window ** (Q + 1))
            den = np.sum(window ** Q)

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
    crow, ccol = rows // 2, cols // 2

    # Costruire il filtro notch
    for u, v in zip(u_k, v_k):
        # Calcolare la distanza euclidea dal punto (u, v) e (-u, -v)
        for i in range(rows):
            for j in range(cols):
                duv = np.sqrt((i - (crow + u)) ** 2 + (j - (ccol + v)) ** 2)
                duv_neg = np.sqrt((i - (crow - u)) ** 2 + (j - (ccol - v)) ** 2)

                if duv < d0 or duv_neg < d0:
                    dft_shift[i, j] = 0  # Elimina queste frequenze

    # Inverti la trasformata di Fourier
    f_ishift = np.fft.ifftshift(dft_shift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    # Convertire a uint8
    return np.clip(img_back, 0, 255).astype(np.uint8)


def shock_filter(image, iterations=10, dt=0.1):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertiamo in grigio
    gray_image = gray_image.astype(np.float32) / 255.0  # Normalizzazione

    for _ in range(iterations):
        laplacian = cv2.Laplacian(gray_image, cv2.CV_32F)
        gradient_x = cv2.Sobel(gray_image, cv2.CV_32F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(gray_image, cv2.CV_32F, 0, 1, ksize=3)
        grad_mag = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

        # Direzione della propagazione dello shock
        sign_lap = np.sign(laplacian)
        gray_image += dt * sign_lap * grad_mag

    gray_image = np.clip(gray_image * 255, 0, 255).astype(np.uint8)
    return cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)  # Converti di nuovo in BGR


def homomorphic_filter(image, low=0.5, high=1.5, cutoff=30):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertiamo in grigio
    image_log = np.log1p(np.array(image, dtype="float") / 255)

    # Trasformata di Fourier
    dft = np.fft.fft2(image_log)
    dft_shift = np.fft.fftshift(dft)

    # Costruzione del filtro passa-basso + passa-alto
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            mask[i, j] = high - (high - low) * np.exp(- (distance ** 2) / (2 * (cutoff ** 2)))

    # Applicazione del filtro e ritorno all'immagine spaziale
    dft_shift_filtered = dft_shift * mask
    dft_filtered = np.fft.ifftshift(dft_shift_filtered)
    image_filtered = np.fft.ifft2(dft_filtered)
    image_filtered = np.real(image_filtered)

    # Conversione finale
    image_exp = np.expm1(image_filtered)
    image_exp = np.clip(image_exp, 0, 1)
    return (image_exp * 255).astype("uint8")


def anisotropic_diffusion(image, iterations=10, k=15, gamma=0.1, option=1):
    """
    Applica il filtro di diffusione anisotropica (Perona-Malik) a un'immagine.

    Args:
        image: L'immagine in input.
        iterations: Numero di iterazioni.
        k: Parametro di sensibilità ai bordi.
        gamma: Fattore di scala per il passo temporale.
        option: Scelta del coefficiente di diffusione (1 o 2).

    Returns:
        L'immagine filtrata.
    """
    # Converti l'immagine in scala di grigi se necessario
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalizza l'immagine tra 0 e 1
    image = image.astype(np.float32) / 255.0

    for _ in range(iterations):
        # Calcola i gradienti nelle quattro direzioni (nord, sud, est, ovest)
        nabla_north = np.roll(image, 1, axis=0) - image
        nabla_south = np.roll(image, -1, axis=0) - image
        nabla_east = np.roll(image, -1, axis=1) - image
        nabla_west = np.roll(image, 1, axis=1) - image

        # Coefficienti di diffusione basati sul gradiente
        if option == 1:
            c_north = np.exp(-(nabla_north / k) ** 2)
            c_south = np.exp(-(nabla_south / k) ** 2)
            c_east = np.exp(-(nabla_east / k) ** 2)
            c_west = np.exp(-(nabla_west / k) ** 2)
        elif option == 2:
            c_north = 1.0 / (1.0 + (nabla_north / k) ** 2)
            c_south = 1.0 / (1.0 + (nabla_south / k) ** 2)
            c_east = 1.0 / (1.0 + (nabla_east / k) ** 2)
            c_west = 1.0 / (1.0 + (nabla_west / k) ** 2)

        # Aggiorna l'immagine
        image += gamma * (
                c_north * nabla_north +
                c_south * nabla_south +
                c_east * nabla_east +
                c_west * nabla_west
        )

    # Ri-scalare i valori da 0 a 255
    image = np.clip(image * 255, 0, 255).astype(np.uint8)

    return image

# altri filtri...
