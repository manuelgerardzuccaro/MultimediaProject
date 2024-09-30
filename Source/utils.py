from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2
import json


def calculate_psnr(original, restored):
    return cv2.PSNR(original, restored)


def calculate_mse(original, restored):
    mse_value = np.mean((original - restored) ** 2)
    return mse_value


def calculate_ssim(original, restored):
    if len(original.shape) == 2:
        original = cv2.cvtColor(original, cv2.COLOR_GRAY2RGB)
    elif original.shape[2] == 4:
        original = cv2.cvtColor(original, cv2.COLOR_BGRA2BGR)

    if len(restored.shape) == 2:
        restored = cv2.cvtColor(restored, cv2.COLOR_GRAY2RGB)
    elif restored.shape[2] == 4:
        restored = cv2.cvtColor(restored, cv2.COLOR_BGRA2BGR)

    if original.shape != restored.shape:
        restored = cv2.resize(restored, (original.shape[1], original.shape[0]))

    min_dim = min(original.shape[0], original.shape[1])

    win_size = min(7, min_dim)

    if win_size % 2 == 0:
        win_size -= 1

    if win_size < 3:
        print("L'immagine è troppo piccola per calcolare l'SSIM. Impostazione di SSIM a 'N/A'.")
        return "N/A"

    ssim_value, _ = ssim(original, restored, full=True, channel_axis=-1, win_size=win_size)
    return ssim_value


def is_grayscale(image):
    if len(image.shape) == 2:
        return True
    elif len(image.shape) == 3 and image.shape[2] == 3:
        # se tutti i canali sono identici
        if np.all(image[:, :, 0] == image[:, :, 1]) and np.all(image[:, :, 0] == image[:, :, 2]):
            return True
    return False


def save_image(image, path):
    cv2.imwrite(path, image)


def save_filter_configuration(filters, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(filters, f)
        print(f"Configurazione salvata con successo in {file_path}")
    except Exception as e:
        print(f"Errore durante il salvataggio della configurazione: {e}")


def load_filter_configuration(file_path):
    try:
        with open(file_path, 'r') as f:
            filters = json.load(f)
        print(f"Configurazione caricata con successo da {file_path}")
        return filters
    except Exception as e:
        print(f"Errore durante il caricamento della configurazione: {e}")
        return None
