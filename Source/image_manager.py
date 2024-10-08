﻿import cv2
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


def load_image(fileName):
    image = cv2.imread(fileName)
    if image is None:
        print("Errore: Immagine non caricata correttamente")
    return image


def save_image(image, path):
    """
    Salva un'immagine OpenCV su disco.

    Args:
        image: L'immagine che deve essere salvata (in formato OpenCV, cioè un array NumPy).
        path: Il percorso completo del file (incluso il nome e l'estensione) dove l'immagine verrà salvata.
    """
    try:
        if image is None:
            print("Errore: Nessuna immagine valida da salvare.")
            return

        success = cv2.imwrite(path, image)

        if success:
            print(f"Immagine salvata correttamente in: {path}")
        else:
            print("Errore durante il salvataggio dell'immagine. Controlla il percorso e i permessi.")
    except Exception as e:
        print(f"Errore durante il salvataggio dell'immagine: {e}")


def convert_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def display_image(image, label):
    height, width, channel = image.shape
    bytes_per_line = 3 * width
    q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

    pixmap = QPixmap.fromImage(q_img)
    label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))


def show_image_fullscreen(image):
    dialog = QDialog()
    dialog.setWindowTitle("Immagine Ingrandita")

    layout = QVBoxLayout(dialog)

    label = QLabel(dialog)
    layout.addWidget(label)

    height, width, channel = image.shape
    bytes_per_line = 3 * width
    q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

    pixmap = QPixmap.fromImage(q_img)

    label.setPixmap(pixmap)

    dialog.setGeometry(100, 100, width, height)

    dialog.exec_()


def show_image_zoomed(image):
    """Mostra l'immagine ingrandita con uno zoom che occupa il 70% dello schermo mantenendo le proporzioni."""
    dialog = QDialog()
    dialog.setWindowTitle("Immagine Ingrandita")

    screen = QApplication.desktop().screenGeometry()
    screen_width, screen_height = screen.width(), screen.height()

    image_height, image_width, _ = image.shape
    aspect_ratio = image_width / image_height

    if aspect_ratio > 1:
        new_width = int(screen_width * 0.7)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = int(screen_height * 0.7)
        new_width = int(new_height * aspect_ratio)

    bytes_per_line = 3 * image_width
    q_img = QImage(image.data, image_width, image_height, bytes_per_line, QImage.Format_RGB888)

    pixmap = QPixmap.fromImage(q_img).scaled(new_width, new_height, Qt.KeepAspectRatio)

    layout = QVBoxLayout(dialog)
    label = QLabel(dialog)
    label.setPixmap(pixmap)
    layout.addWidget(label)

    dialog.setGeometry(100, 100, new_width, new_height)

    dialog.exec_()