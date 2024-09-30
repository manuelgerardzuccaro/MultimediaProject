import cv2
import numpy as np
from scipy.ndimage import convolve
from scipy.signal import wiener
from utils import is_grayscale


def median_filter(image, ksize):
    if ksize <= 1:
        ksize = 3

    # ksize deve essere dispari
    if ksize % 2 == 0:
        ksize += 1

    pad_size = ksize // 2

    if is_grayscale(image):  # immagine in scala di grigi
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

    # Creato un kernel di dimensione kernel_size X kernel_size
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)

    if is_grayscale(image):  # immagine in scala di grigi
        return cv2.filter2D(image, -1, kernel)
    else:  # immagine a colori
        channels = cv2.split(image)
        filtered_channels = [cv2.filter2D(channel, -1, kernel) for channel in channels]
        return cv2.merge(filtered_channels)


def geometric_mean_filter(image, kernel_size=3):
    if kernel_size < 1:
        kernel_size = 3
    if kernel_size % 2 == 0:
        kernel_size += 1

    pad_size = kernel_size // 2
    epsilon = 1e-5  # piccolo valore per evitare log(0)

    if is_grayscale(image): # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    filtered_channels = []
    for img in images:
        padded_image = cv2.copyMakeBorder(img, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
        output = np.zeros_like(img, dtype=np.float32)

        for i in range(pad_size, padded_image.shape[0] - pad_size):
            for j in range(pad_size, padded_image.shape[1] - pad_size):
                window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1].astype(np.float32)
                product = np.prod(window + epsilon)
                geometric_mean = product ** (1.0 / (kernel_size * kernel_size))
                output[i - pad_size, j - pad_size] = geometric_mean

        output = np.clip(output, 0, 255).astype(np.uint8)
        filtered_channels.append(output)

    return cv2.merge(filtered_channels) if len(filtered_channels) > 1 else filtered_channels[0]


# non funzionante
def log_geometric_mean_filter(image, kernel_size=3):
    if kernel_size < 1:
        kernel_size = 3

    if kernel_size % 2 == 0:
        kernel_size += 1

    pad_size = kernel_size // 2  # divisione intera
    epsilon = 1e-5  # piccolo valore per evitare log(0)

    if is_grayscale(image):  # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    filtered_channels = []
    for img in images:
        padded_image = cv2.copyMakeBorder(img, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
        filtered_image = np.zeros_like(img, dtype=np.float32)

        for i in range(pad_size, padded_image.shape[0] - pad_size):
            for j in range(pad_size, padded_image.shape[1] - pad_size):
                window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1].astype(np.float32)
                log_sum = np.sum(np.log(window + epsilon))
                geometric_mean = np.exp(log_sum / (kernel_size * kernel_size))
                filtered_image[i - pad_size, j - pad_size] = geometric_mean

        filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
        filtered_channels.append(filtered_image)

    return cv2.merge(filtered_channels) if len(filtered_channels) > 1 else filtered_channels[0]


def gaussian_filter(image, kernel_size=5, sigma=1.0):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


def contra_harmonic_mean_filter(image, kernel_size=3, Q=1.0):
    if kernel_size < 1:
        kernel_size = 3
    if kernel_size % 2 == 0:
        kernel_size += 1

    pad_size = kernel_size // 2

    if is_grayscale(image):  # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    filtered_channels = []
    for img in images:
        padded_image = cv2.copyMakeBorder(img, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
        filtered_image = np.zeros_like(img, dtype=np.float32)

        for i in range(pad_size, padded_image.shape[0] - pad_size):
            for j in range(pad_size, padded_image.shape[1] - pad_size):
                window = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
                window = np.where(window == 0, 1e-10, window)
                num = np.sum(window ** (Q + 1))
                den = np.sum(window ** Q)

                if den != 0 and not np.isnan(den):
                    filtered_image[i - pad_size, j - pad_size] = num / den
                else:
                    filtered_image[i - pad_size, j - pad_size] = 0

        filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
        filtered_channels.append(filtered_image)

    return cv2.merge(filtered_channels) if len(filtered_channels) > 1 else filtered_channels[0]


def notch_filter(image, d0, u_k, v_k):
    if not is_grayscale(image):
        channels = cv2.split(image)
        filtered_channels = []

        for ch in channels:
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

            dft_shift_filtered = dft_shift * mask

            # inversa della trasformata di Fourier
            f_ishift = np.fft.ifftshift(dft_shift_filtered)
            img_back = np.fft.ifft2(f_ishift)
            img_back = np.abs(img_back)

            filtered_channels.append(np.clip(img_back, 0, 255).astype(np.uint8))

        return cv2.merge(filtered_channels)

    else:  # immagine in scala di grigi
        dft = np.fft.fft2(image)
        dft_shift = np.fft.fftshift(dft)

        rows, cols = image.shape
        crow, ccol = rows // 2, cols // 2

        mask = np.ones((rows, cols), np.float32)

        for u, v in zip(u_k, v_k):
            for i in range(rows):
                for j in range(cols):
                    duv = np.sqrt((i - (crow + u)) ** 2 + (j - (ccol + v)) ** 2)
                    duv_neg = np.sqrt((i - (crow - u)) ** 2 + (j - (ccol - v)) ** 2)

                    if duv < d0 or duv_neg < d0:
                        mask[i, j] = 0

        dft_shift_filtered = dft_shift * mask

        # inversa della trasformata di Fourier
        f_ishift = np.fft.ifftshift(dft_shift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)

        return np.clip(img_back, 0, 255).astype(np.uint8)


def shock_filter(image, iterations=10, dt=0.1):
    if is_grayscale(image): # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    filtered_channels = []
    for img in images:
        img_float = img.astype(np.float32) / 255.0

        for _ in range(iterations):
            laplacian = cv2.Laplacian(img_float, cv2.CV_32F)
            gradient_x = cv2.Sobel(img_float, cv2.CV_32F, 1, 0, ksize=3)
            gradient_y = cv2.Sobel(img_float, cv2.CV_32F, 0, 1, ksize=3)
            grad_mag = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

            # direzione della propagazione dello shock
            sign_lap = np.sign(laplacian)
            img_float += dt * sign_lap * grad_mag

        img_filtered = np.clip(img_float * 255, 0, 255).astype(np.uint8)
        filtered_channels.append(img_filtered)

    return cv2.merge(filtered_channels) if len(filtered_channels) > 1 else filtered_channels[0]


def homomorphic_filter(image, low=0.5, high=1.5, cutoff=30):
    if is_grayscale(image):  # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    filtered_channels = []
    for img in images:
        image_log = np.log1p(np.array(img, dtype="float") / 255)

        dft = np.fft.fft2(image_log)
        dft_shift = np.fft.fftshift(dft)

        rows, cols = img.shape
        crow, ccol = rows // 2, cols // 2

        mask = np.ones((rows, cols), np.float32)
        for i in range(rows):
            for j in range(cols):
                distance = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
                mask[i, j] = high - (high - low) * np.exp(- (distance ** 2) / (2 * (cutoff ** 2)))

        dft_shift_filtered = dft_shift * mask
        dft_filtered = np.fft.ifftshift(dft_shift_filtered)
        image_filtered = np.fft.ifft2(dft_filtered)
        image_filtered = np.real(image_filtered)

        image_exp = np.expm1(image_filtered)
        image_exp = np.clip(image_exp, 0, 1)
        filtered_channels.append((image_exp * 255).astype("uint8"))

    return cv2.merge(filtered_channels) if len(filtered_channels) > 1 else filtered_channels[0]


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
    if not is_grayscale(image):
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
    if is_grayscale(image):  # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    restored_channels = []
    for img in images:
        # filtro mediano preliminare per ridurre il rumore "sale e pepe"
        img = cv2.medianBlur(img, 3)

        # Normalizzazione dell'immagine
        img = img.astype(np.float32) / 255.0

        restored_image = img.copy()

        # Kernel per la convoluzione (gaussiano)
        kernel = np.array([[1, 2, 1],
                           [2, 4, 2],
                           [1, 2, 1]]) / 16

        for _ in range(iterations):
            blurred_image = convolve(restored_image, kernel)

            # Gradiente per la regolarizzazione TV
            gradient_x = np.roll(restored_image, -1, axis=1) - restored_image
            gradient_y = np.roll(restored_image, -1, axis=0) - restored_image
            tv_term = np.sqrt(gradient_x ** 2 + gradient_y ** 2 + 1e-5)

            fidelity_term = blurred_image - img
            fidelity_term = np.clip(fidelity_term, -0.1, 0.1)  # Applicazione di soglia

            update_term = regularization_weight * (fidelity_term / (tv_term + 1e-8))
            restored_image -= update_term

        # Ri-scalatura dei valori dell'immagine e ritorno al formato uint8
        restored_image = np.clip(restored_image * 255, 0, 255).astype(np.uint8)
        restored_channels.append(restored_image)

    # Combina i canali nel caso di un'immagine a colori, altrimenti restituisce il canale singolo
    return cv2.merge(restored_channels) if len(restored_channels) > 1 else restored_channels[0]


def wiener_deconvolution(image, kernel_size=5, noise=0.01):
    epsilon = 1e-5  # Piccolo valore per prevenire divisioni per zero
    pad_size = kernel_size // 2  # Determina la dimensione del padding

    if is_grayscale(image):  # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    deconvolved_channels = []
    for img in images:
        padded_image = cv2.copyMakeBorder(img, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)

        # Normalizza l'immagine nell'intervallo [0, 1]
        padded_image = padded_image.astype(np.float32) / 255.0

        deconvolved_img = wiener(padded_image, (kernel_size, kernel_size), noise + epsilon)

        # Gestione di NaN e valori infiniti
        deconvolved_img = np.nan_to_num(deconvolved_img)

        # Rimuovi il padding
        deconvolved_img = deconvolved_img[pad_size:-pad_size, pad_size:-pad_size]

        # Riportare i valori nell'intervallo [0, 1]
        deconvolved_img = np.clip(deconvolved_img, 0, 1)

        deconvolved_img = (deconvolved_img * 255).astype(np.uint8)
        deconvolved_channels.append(deconvolved_img)

    # Ricombina i canali nel caso di un'immagine a colori, altrimenti restituisce il canale singolo
    return cv2.merge(deconvolved_channels) if len(deconvolved_channels) > 1 else deconvolved_channels[0]


# altri filtri...


# rumori

def add_gaussian_noise(image, mean=0, std_dev=25):
    if is_grayscale(image):  # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    noisy_channels = []
    for img in images:
        img_float = img.astype(np.float32)
        noise = np.random.normal(mean, std_dev, img.shape).astype(np.float32)
        noisy_img = img_float + noise
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)
        noisy_channels.append(noisy_img)

    return cv2.merge(noisy_channels) if len(noisy_channels) > 1 else noisy_channels[0]


def add_salt_pepper_noise(image, prob=0.05):
    # Crea una copia dell'immagine
    noisy_image = image.copy()

    # Numero di pixel da modificare
    num_salt = int(np.ceil(prob * image.size * 0.5))
    num_pepper = int(np.ceil(prob * image.size * 0.5))

    # Aggiungi "sale" (bianco)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
    if is_grayscale(image): # immagine in scala di grigi
        noisy_image[coords[0], coords[1]] = 255
    else:  # immagine a colori
        noisy_image[coords[0], coords[1], :] = 255

    # Aggiungi "pepe" (nero)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
    if is_grayscale(image): # immagine in scala di grigi
        noisy_image[coords[0], coords[1]] = 0
    else:  # immagine a colori
        noisy_image[coords[0], coords[1], :] = 0

    return noisy_image


def add_uniform_noise(image, low=0, high=50):
    if is_grayscale(image):  # immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    noisy_channels = []
    for img in images:
        noise = np.random.uniform(low, high, img.shape).astype(np.uint8)
        noisy_img = cv2.add(img, noise)
        noisy_channels.append(noisy_img)

    return cv2.merge(noisy_channels) if len(noisy_channels) > 1 else noisy_channels[0]


def add_film_grain_noise(image, std_dev=20):
    if is_grayscale(image):  # immagine in scala di grigi
        row, col = image.shape
        noise = np.random.normal(0, std_dev, (row, col)).astype(np.int16)
        img_int16 = image.astype(np.int16)
        noisy_img = cv2.add(img_int16, noise)
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)
        return noisy_img

    else:  # immagine a colori
        images = cv2.split(image)
        noisy_channels = []
        for img in images:
            row, col = img.shape
            noise = np.random.normal(0, std_dev, (row, col)).astype(np.int16)
            img_int16 = img.astype(np.int16)
            noisy_img = cv2.add(img_int16, noise)
            noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)
            noisy_channels.append(noisy_img)

        return cv2.merge(noisy_channels)


def add_periodic_noise(image, amplitude=50, frequency=40):
    if is_grayscale(image):  # Immagine in scala di grigi
        images = [image]
    else:  # immagine a colori
        images = cv2.split(image)

    noisy_channels = []
    for img in images:
        noisy_img = img.astype(np.float32)
        row, col = img.shape

        # Crea il rumore periodico (sinusoidale) lungo la larghezza con una data frequenza
        periodic_noise = np.sin(np.linspace(0, 2 * np.pi * frequency, col))

        # Estendi il rumore periodico lungo l'altezza dell'immagine
        periodic_noise = np.tile(periodic_noise, (row, 1))

        # Aggiungi il rumore al canale dell'immagine
        noisy_img += (periodic_noise * amplitude)
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)
        noisy_channels.append(noisy_img)

    return cv2.merge(noisy_channels) if len(noisy_channels) > 1 else noisy_channels[0]

# altri rumori...
