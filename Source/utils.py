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
    # Assicurati che entrambe le immagini siano RGB
    if len(original.shape) == 2:
        original = cv2.cvtColor(original, cv2.COLOR_GRAY2RGB)
    elif original.shape[2] == 4:  # Se l'immagine ha un canale alfa
        original = cv2.cvtColor(original, cv2.COLOR_BGRA2BGR)

    if len(restored.shape) == 2:
        restored = cv2.cvtColor(restored, cv2.COLOR_GRAY2RGB)
    elif restored.shape[2] == 4:  # Se l'immagine ha un canale alfa
        restored = cv2.cvtColor(restored, cv2.COLOR_BGRA2BGR)

    # Assicurati che le dimensioni delle immagini siano le stesse
    if original.shape != restored.shape:
        restored = cv2.resize(restored, (original.shape[1], original.shape[0]))

    # Determina la dimensione minima tra altezza e larghezza dell'immagine
    min_dim = min(original.shape[0], original.shape[1])

    # Imposta win_size a un valore dispari e minore o uguale alla dimensione minima
    win_size = min(7, min_dim)

    # Assicura che win_size sia un numero dispari
    if win_size % 2 == 0:
        win_size -= 1

    # Gestisci il caso in cui l'immagine sia ancora troppo piccola
    if win_size < 3:
        print("L'immagine è troppo piccola per calcolare l'SSIM. Impostazione di SSIM a 'N/A'.")
        return "N/A"

    # Calcola l'SSIM con il win_size adattato
    ssim_value, _ = ssim(original, restored, full=True, channel_axis=-1, win_size=win_size)
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
