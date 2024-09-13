from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2

def load_image(fileName):
    image = cv2.imread(fileName)
    if image is None:
        print("Errore: Immagine non caricata correttamente")
    return image

def convert_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def display_image(image, label):
    height, width, channel = image.shape
    bytes_per_line = 3 * width
    q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

    pixmap = QPixmap.fromImage(q_img)
    label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))
