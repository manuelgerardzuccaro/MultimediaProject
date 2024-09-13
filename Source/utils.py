import cv2
import json

def calculate_psnr(original, restored):
    return cv2.PSNR(original, restored)

def save_image(image, path):
    cv2.imwrite(path, image)

def save_filter_configuration(filters, file_path):
    """Salva la configurazione dei filtri in un file JSON."""
    try:
        with open(file_path, 'w') as f:
            json.dump(filters, f)
        print(f"Configurazione salvata con successo in {file_path}")
    except Exception as e:
        print(f"Errore durante il salvataggio della configurazione: {e}")

def load_filter_configuration(file_path):
    """Carica la configurazione dei filtri da un file JSON."""
    try:
        with open(file_path, 'r') as f:
            filters = json.load(f)
        print(f"Configurazione caricata con successo da {file_path}")
        return filters
    except Exception as e:
        print(f"Errore durante il caricamento della configurazione: {e}")
        return None