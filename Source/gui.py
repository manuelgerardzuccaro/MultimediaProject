from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QWidget
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
        self.setGeometry(100, 100, 1200, 600)  # Impostiamo una finestra più grande

        # Layout principale verticale
        self.layout = QVBoxLayout()

        # Layout orizzontale per le immagini
        self.image_layout = QHBoxLayout()

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
        self.slider.setMinimum(3)
        self.slider.setMaximum(15)
        self.slider.setValue(5)
        self.layout.addWidget(self.slider)

        # Aree di visualizzazione delle immagini (originale e restaurata)
        self.original_label = QLabel(self)
        self.restored_label = QLabel(self)

        # Impostiamo una dimensione fissa più grande per le immagini
        self.original_label.setFixedSize(500, 400)
        self.restored_label.setFixedSize(500, 400)

        # Aggiungiamo le etichette al layout delle immagini affiancate
        self.image_layout.addWidget(self.original_label)
        self.image_layout.addWidget(self.restored_label)

        # Aggiungiamo il layout delle immagini al layout principale
        self.layout.addLayout(self.image_layout)

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

            # Convertiamo l'immagine in RGB per la visualizzazione
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb, self.original_label)

    def apply_filter(self):
        selected_filter = self.filter_combo.currentText()

        if selected_filter == "Filtro Mediano":
            ksize = self.slider.value() * 2 + 1  # Numero dispari per il filtro mediano
            self.restored_image = median_filter(self.image, ksize)

        elif selected_filter == "Filtro Media Aritmetica":
            kernel_size = self.slider.value()  # Dimensione del kernel per la media aritmetica
            self.restored_image = mean_filter(self.image, kernel_size)  # Applica il filtro di media aritmetica

        # Verifica che self.restored_image sia stato definito prima di convertire
        if self.restored_image is not None:
            # Converti l'immagine restaurata da BGR a RGB prima della visualizzazione
            image_rgb = cv2.cvtColor(self.restored_image, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb, self.restored_label)
        else:
            print("Errore: il filtro non è stato applicato correttamente.")

    def display_image(self, image, label):
        # Converti l'immagine in QImage
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Converti QImage in QPixmap e visualizza
        pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))
