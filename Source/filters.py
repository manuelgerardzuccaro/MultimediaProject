﻿import cv2
import numpy as np
from scipy.ndimage import convolve
from scipy.signal import wiener


def median_filter(image, ksize):
    if ksize <= 1:
        ksize = 3

    # ksize deve essere dispari
    if ksize % 2 == 0:
        ksize += 1

    pad_size = ksize // 2

    if len(image.shape) == 2:  # immagine in scala di grigi
        padded_image = cv2.copyMakeBorder(image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
        filtered_image = np.zeros_like(image)

        for i in range(pad_size, padded_image.shape[0] - pad_size):
            for j in range(pad_size, padded_image.shape[1] - pad_size):
                window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                median_value = np.median(window)
                filtered_image[i - pad_size, j - pad_size] = median_value

    else:  # immagine a colori
        filtered_image = np.zeros_like(image)
        for c in range(image.shape[2]):  # si itera sui canali (R, G, B)
            padded_image = cv2.copyMakeBorder(image[:, :, c], pad_size, pad_size, pad_size, pad_size,
                                              cv2.BORDER_REFLECT)

            for i in range(pad_size, padded_image.shape[0] - pad_size):
                for j in range(pad_size, padded_image.shape[1] - pad_size):
                    window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                    median_value = np.median(window)
                    filtered_image[i - pad_size, j - pad_size, c] = median_value

    return filtered_image


def median_blur_filter(image, ksize):
    if ksize <= 1:
        ksize = 3

    # ksize deve essere dispari
    if ksize % 2 == 0:
        ksize += 1

    # uso di medianBlur di OpenCV
    return cv2.medianBlur(image, ksize)


def mean_filter(image, kernel_size=3):
    if kernel_size <= 1:
        kernel_size = 3  # dimensione di default

    if kernel_size % 2 == 0:
        kernel_size += 1  # kernel_size dispari

    # creato un Kernel di dim: kernel_size X kernel_size, riempito di 1;
    # che viene normalizzato dividendo ogni elemento per (kernel_size^2)
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)

    # convoluzione
    return cv2.filter2D(image, -1, kernel)


def geometric_mean_filter(image, kernel_size=3):
    if kernel_size < 1:
        kernel_size = 3
    if kernel_size % 2 == 0:
        kernel_size += 1

    pad_size = kernel_size // 2

    # piccolo valore per evitare log(0)
    epsilon = 1e-5

    # conversione in scala di grigi (se è a colori)
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    padded_image = cv2.copyMakeBorder(image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
    output = np.zeros_like(image, dtype=np.float32)

    for i in range(pad_size, padded_image.shape[0] - pad_size):
        for j in range(pad_size, padded_image.shape[1] - pad_size):
            window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1].astype(np.float32)

            product = np.prod(window + epsilon)  # + epsilon per evitare problemi con pixel a zero

            geometric_mean = product ** (1.0 / (kernel_size * kernel_size))

            output[i - pad_size, j - pad_size] = geometric_mean

    output = np.clip(output, 0, 255).astype(np.uint8)

    return output


# non funzionante
def log_geometric_mean_filter(image, kernel_size=3):
    if kernel_size < 1:
        kernel_size = 3

    if kernel_size % 2 == 0:
        kernel_size += 1

    pad_size = kernel_size // 2  # divisione intera

    padded_image = cv2.copyMakeBorder(image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)

    filtered_image = np.zeros_like(image, dtype=np.float32)

    # piccolo valore per evitare log(0)
    epsilon = 1e-5

    for i in range(pad_size, padded_image.shape[0] - pad_size):
        for j in range(pad_size, padded_image.shape[1] - pad_size):
            window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1].astype(np.float32)
            log_sum = np.sum(np.log(window + epsilon))  # somma dei logaritmi
            geometric_mean = np.exp(log_sum / (kernel_size * kernel_size))
            filtered_image[i - pad_size, j - pad_size] = geometric_mean

    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)

    return filtered_image


def gaussian_filter(image, kernel_size=5, sigma=1.0):
    # Assicura che il kernel sia un numero dispari
    if kernel_size % 2 == 0:
        kernel_size += 1
    # Applica il filtro gaussiano
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


def contra_harmonic_mean_filter(image, kernel_size=3, Q=1.0):
    if kernel_size < 1:
        kernel_size = 3

    # Assicura che il kernel sia dispari
    if kernel_size % 2 == 0:
        kernel_size += 1

    pad_size = kernel_size // 2
    padded_image = cv2.copyMakeBorder(image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)

    filtered_image = np.zeros_like(image, dtype=np.float32)

    for i in range(pad_size, padded_image.shape[0] - pad_size):
        for j in range(pad_size, padded_image.shape[1] - pad_size):
            window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]

            # Evita problemi con divisioni per zero, sostituendo i valori 0 con un piccolo numero
            window = np.where(window == 0, 1e-10, window)  # Sostituisci 0 con un numero piccolo

            num = np.sum(window ** (Q + 1))
            den = np.sum(window ** Q)

            # Gestisce casi in cui den è 0 o non valido
            if den != 0 and not np.isnan(den):
                filtered_image[i - pad_size, j - pad_size] = num / den
            else:
                filtered_image[i - pad_size, j - pad_size] = 0

    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image


def notch_filter(image, d0, u_k, v_k):
    # Controlla se l'immagine ha 3 canali (colori)
    if len(image.shape) == 3:
        # Separa i canali (B, G, R)
        channels = cv2.split(image)
        filtered_channels = []

        for ch in channels:
            # Applica il filtro notch al canale
            dft = np.fft.fft2(ch)
            dft_shift = np.fft.fftshift(dft)

            rows, cols = ch.shape
            crow, ccol = rows // 2, cols // 2

            # Crea la maschera
            mask = np.ones((rows, cols), np.float32)

            for u, v in zip(u_k, v_k):
                for i in range(rows):
                    for j in range(cols):
                        duv = np.sqrt((i - (crow + u)) ** 2 + (j - (ccol + v)) ** 2)
                        duv_neg = np.sqrt((i - (crow - u)) ** 2 + (j - (ccol - v)) ** 2)

                        if duv < d0 or duv_neg < d0:
                            mask[i, j] = 0

            # Applica la maschera
            dft_shift_filtered = dft_shift * mask

            # Inversa della trasformata di Fourier
            f_ishift = np.fft.ifftshift(dft_shift_filtered)
            img_back = np.fft.ifft2(f_ishift)
            img_back = np.abs(img_back)

            # Aggiungi il canale filtrato alla lista
            filtered_channels.append(np.clip(img_back, 0, 255).astype(np.uint8))

        # Combina i canali filtrati in un'unica immagine a colori
        return cv2.merge(filtered_channels)

    else:  # Immagine in scala di grigi
        # Applica il filtro direttamente
        dft = np.fft.fft2(image)
        dft_shift = np.fft.fftshift(dft)

        rows, cols = image.shape
        crow, ccol = rows // 2, cols // 2

        # Crea la maschera
        mask = np.ones((rows, cols), np.float32)

        for u, v in zip(u_k, v_k):
            for i in range(rows):
                for j in range(cols):
                    duv = np.sqrt((i - (crow + u)) ** 2 + (j - (ccol + v)) ** 2)
                    duv_neg = np.sqrt((i - (crow - u)) ** 2 + (j - (ccol - v)) ** 2)

                    if duv < d0 or duv_neg < d0:
                        mask[i, j] = 0

        # Applica la maschera
        dft_shift_filtered = dft_shift * mask

        # Inversa della trasformata di Fourier
        f_ishift = np.fft.ifftshift(dft_shift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)

        return np.clip(img_back, 0, 255).astype(np.uint8)


def shock_filter(image, iterations=10, dt=0.1):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # in scala di grigio
    gray_image = gray_image.astype(np.float32) / 255.0  # normalizzazione

    for _ in range(iterations):
        laplacian = cv2.Laplacian(gray_image, cv2.CV_32F)
        gradient_x = cv2.Sobel(gray_image, cv2.CV_32F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(gray_image, cv2.CV_32F, 0, 1, ksize=3)
        grad_mag = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

        # direzione della propagazione dello shock
        sign_lap = np.sign(laplacian)
        gray_image += dt * sign_lap * grad_mag

    gray_image = np.clip(gray_image * 255, 0, 255).astype(np.uint8)
    return cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)


def homomorphic_filter(image, low=0.5, high=1.5, cutoff=30):
    """
    low e high sono i fattori che determinano la quantità di amplificazione o attenuazione delle basse e alte frequenze.

    cutoff è il parametro che controlla la dimensione della regione a bassa frequenza nel centro dello spettro.
        Un valore più alto rende il filtro meno sensibile alle basse frequenze
   """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # in scala di grigio
    image_log = np.log1p(np.array(image, dtype="float") / 255)

    # trasformata di Fourier
    dft = np.fft.fft2(image_log)
    dft_shift = np.fft.fftshift(dft)

    # filtro passa_basso + passa_alto
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2

    mask = np.ones((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            mask[i, j] = high - (high - low) * np.exp(- (distance ** 2) / (2 * (cutoff ** 2)))

    # applicazione del filtro e ritorno all'immagine spaziale
    dft_shift_filtered = dft_shift * mask
    dft_filtered = np.fft.ifftshift(dft_shift_filtered)
    image_filtered = np.fft.ifft2(dft_filtered)
    image_filtered = np.real(image_filtered)

    # conversione
    image_exp = np.expm1(image_filtered)
    image_exp = np.clip(image_exp, 0, 1)
    return (image_exp * 255).astype("uint8")


def anisotropic_diffusion(image, iterations=10, k=15, gamma=0.1, option=1):
    """
    Applica il filtro di diffusione anisotropica (Perona-Malik) a un'immagine.
    Efficace nel correggere rumore additivo di tipo gaussiano

    Funziona per immagini a colori separando i canali.

    - Iterations: Un numero più basso di iterazioni se si vuole mantenere i dettagli, mentre un numero più alto se il
        rumore è molto forte

    - K (Sensibilità al gradiente): determina quanto l'algoritmo sarà capace di distinguere tra il rumore e i dettagli/bordi

    - Gamma (Fattore di velocità della diffusione): Controlla la quantità di modifica applicata ai pixel a ogni iterazione,
        valori troppo alti possono causare instabilità e artefatti

    - Option 1 (Funzione Esponenziale): Quando il mantenimento dei bordi è una priorità assoluta e quando si ha
        un'immagine con dettagli nitidi che non devono essere sfocati.

    - Option 2 (Funzione Razionale): Quando si desidera una riduzione del rumore più uniforme e non si è troppo
        preoccupati di preservare bordi molto netti. È utile per immagini dove i dettagli sono meno definiti o dove si
        cerca un compromesso tra riduzione del rumore e mantenimento dei bordi.
    """

    # se immagine a colori (canali separati)
    if len(image.shape) == 3:
        b, g, r = cv2.split(image)

        # applicazione del filtro anisotropic su ciascun canale
        b_filtered = anisotropic_diffusion_single_channel(b, iterations, k, gamma, option)
        g_filtered = anisotropic_diffusion_single_channel(g, iterations, k, gamma, option)
        r_filtered = anisotropic_diffusion_single_channel(r, iterations, k, gamma, option)

        # ricombinare i canali filtrati
        return cv2.merge([b_filtered, g_filtered, r_filtered])

    # se immagine in scala di grigi
    return anisotropic_diffusion_single_channel(image, iterations, k, gamma, option)


def anisotropic_diffusion_single_channel(channel, iterations, k, gamma, option):
    """
    Applica la diffusione anisotropica su un singolo canale di immagine in scala di grigi.
    """
    # normalizzazione tra 0 e 1
    channel = channel.astype(np.float32) / 255.0

    for _ in range(iterations):
        # calcolo dei gradienti
        nabla_north = np.roll(channel, 1, axis=0) - channel
        nabla_south = np.roll(channel, -1, axis=0) - channel
        nabla_east = np.roll(channel, -1, axis=1) - channel
        nabla_west = np.roll(channel, 1, axis=1) - channel

        # calcolo dei coefficienti di diffusione
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

        channel += gamma * (
                c_north * nabla_north +
                c_south * nabla_south +
                c_east * nabla_east +
                c_west * nabla_west
        )

    # ri-scalatura dei valori da 0 a 255
    channel = np.clip(channel * 255, 0, 255).astype(np.uint8)

    return channel


def l1_tv_deconvolution(image, iterations=30, regularization_weight=0.05):
    # conversione in scala di grigi (se è a colori)
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # filtro mediano preliminare per ridurre il rumore "sale e pepe"
    image = cv2.medianBlur(image, 3)

    # normalizzazione dell'immagine
    image = image.astype(np.float32) / 255.0

    restored_image = image.copy()

    # kernel per la convoluzione (gaussiano)
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]]) / 16

    for _ in range(iterations):
        blurred_image = convolve(restored_image, kernel)

        # gradiente per la regolarizzazione TV
        gradient_x = np.roll(restored_image, -1, axis=1) - restored_image
        gradient_y = np.roll(restored_image, -1, axis=0) - restored_image
        tv_term = np.sqrt(gradient_x ** 2 + gradient_y ** 2 + 1e-5)

        fidelity_term = blurred_image - image
        fidelity_term = np.clip(fidelity_term, -0.1, 0.1)  # Applicazione di soglia

        update_term = regularization_weight * (fidelity_term / (tv_term + 1e-8))
        restored_image -= update_term

    # ri-scalatura dei valori dell'immagine e ritorno al formato uint8
    restored_image = np.clip(restored_image * 255, 0, 255).astype(np.uint8)

    return restored_image


def wiener_deconvolution(image, kernel_size=5):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # applicazione del filtro di Wiener per la deconvoluzione
    deconvolved_image = wiener(image, (kernel_size, kernel_size))

    # normalizzazione e conversione in uint8
    deconvolved_image = np.clip(deconvolved_image * 255, 0, 255).astype(np.uint8)

    return deconvolved_image


# altri filtri...


# rumori

def add_gaussian_noise(image, mean=0, std_dev=25):
    # Converti l'immagine in formato float32 per evitare overflow durante l'aggiunta del rumore
    image_float = image.astype(np.float32)

    # Crea il rumore gaussiano
    noise = np.random.normal(mean, std_dev, image.shape).astype(np.float32)

    # Aggiungi il rumore all'immagine
    noisy_image = image_float + noise

    # Clipping per assicurare che i valori siano nel range [0, 255]
    noisy_image = np.clip(noisy_image, 0, 255)

    # Converti nuovamente l'immagine in uint8
    return noisy_image.astype(np.uint8)


def add_salt_pepper_noise(image):
    prob = 0.05  # probabilità di sale e pepe
    noisy_image = image.copy()

    # sale (pixel bianchi)
    num_salt = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 255

    # pepe (pixel neri)
    num_pepper = np.ceil(prob * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 0

    return noisy_image


def add_uniform_noise(image):
    noise = np.random.uniform(0, 50, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, noise)
    return noisy_image


def add_film_grain_noise(image):
    row, col, ch = image.shape
    gauss = np.random.normal(0, 20, (row, col, ch)).astype(np.uint8)
    noisy_image = cv2.add(image, gauss)
    return noisy_image


def add_periodic_noise(image, amplitude=150):
    # Crea un'immagine float per evitare overflow
    noisy_image = image.astype(np.float32)

    # Dimensioni dell'immagine
    row, col, ch = image.shape

    # Crea il rumore periodico (sinusoidale) lungo la larghezza
    periodic_noise = np.sin(np.linspace(0, 2 * np.pi, col))

    # Estendi il rumore periodico lungo l'altezza dell'immagine
    periodic_noise = np.tile(periodic_noise, (row, 1))

    # Aggiungi il rumore a ogni canale dell'immagine
    for i in range(ch):
        noisy_image[:, :, i] += (periodic_noise * amplitude)

    # Clippa i valori per essere nell'intervallo [0, 255]
    noisy_image = np.clip(noisy_image, 0, 255)

    # Converti nuovamente a uint8
    return noisy_image.astype(np.uint8)

# altri rumori...
