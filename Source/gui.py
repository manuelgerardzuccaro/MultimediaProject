from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QComboBox, QSlider, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from filters import median_filter, mean_filter  # Importa i filtri dal file filters.py

class ImageRestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Restauro Immagini - Riduzione Rumore')

        # Layout principale
        self.layout = QVBoxLayout()

        # Bottone per il caricamento dell'immagine
        self.load_button = QPushButton('Carica Immagine', self)
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        # Menu a tendina per la selezione del filtro
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["Filtro Mediano", "Filtro Media Aritmetica"])
        self.layout.addWidget(self.filter_combo)

        # Bottone per applicare il filtro
        self.apply_button = QPushButton('Applica Filtro', self)
        self.apply_button.clicked.connect(self.apply_filter)
        self.layout.addWidget(self.apply_button)

        # Slider per la dimensione del filtro
        self.slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.slider)

        # Aree di visualizzazione delle immagini
        self.original_label = QLabel(self)
        self.restored_label = QLabel(self)
        self.layout.addWidget(self.original_label)
        self.layout.addWidget(self.restored_label)

        # Widget principale
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica Immagine", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if fileName:
            # Carica l'immagine
            self.image = cv2.imread(fileName)

            # Controlla se l'immagine è stata caricata correttamente
            if self.image is None:
                print("Errore: Immagine non caricata correttamente")
                return

            self.display_image(self.image, self.original_label)

    def apply_filter(self):
        selected_filter = self.filter_combo.currentText()
        if selected_filter == "Filtro Mediano":
            self.restored_image = median_filter(self.image, self.slider.value())
        elif selected_filter == "Filtro Media Aritmetica":
            self.restored_image = mean_filter(self.image)

        self.display_image(self.restored_image, self.restored_label)

    def display_image(self, image, label):
        # Converti l'immagine OpenCV (BGR) in RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Converti l'immagine in QImage
        height, width, channel = image_rgb.shape
        bytes_per_line = 3 * width
        q_img = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Converti QImage in QPixmap e visualizza
        pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))

