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
    ssim_value, _ = ssim(original, restored, full=True, multichannel=True)
    return ssim_value


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
