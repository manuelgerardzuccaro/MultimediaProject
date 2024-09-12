from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QWidget, QListWidget, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
import cv2
import numpy as np
from filters import median_filter, mean_filter  # Importa i filtri dal file filters.py

class ImageRestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.applied_filters = []  # Lista per memorizzare i filtri applicati

    def initUI(self):
        self.setWindowTitle('Restauro Immagini - Riduzione Rumore')
        self.setGeometry(100, 100, 1600, 900)  # Finestra più grande

        # Layout principale verticale
        self.layout = QVBoxLayout()

        # Layout orizzontale per le immagini
        self.image_layout = QHBoxLayout()

        # Font personalizzato per aumentare la dimensione del testo
        large_font = QFont("Arial", 12)  # Font size increased

        # Bottone per il caricamento dell'immagine con icona
        self.load_button = QPushButton('Carica Immagine', self)
        self.load_button.setFont(large_font)
        self.load_button.setIcon(QIcon('load_icon.png'))  # Assumi che tu abbia un'icona chiamata load_icon.png
        self.load_button.setIconSize(QSize(32, 32))
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        # Menu a tendina per la selezione del filtro
        self.filter_combo = QComboBox(self)
        self.filter_combo.setFont(large_font)
        self.filter_combo.addItems(["Filtro Mediano", "Filtro Media Aritmetica"])
        self.layout.addWidget(self.filter_combo)

        # Bottone per applicare il filtro con icona
        self.apply_button = QPushButton('Applica Filtro', self)
        self.apply_button.setFont(large_font)
        self.apply_button.setIcon(QIcon('apply_icon.png'))  # Assumi che tu abbia un'icona chiamata apply_icon.png
        self.apply_button.setIconSize(QSize(32, 32))
        self.apply_button.clicked.connect(self.apply_filter)
        self.layout.addWidget(self.apply_button)

        # Slider per la dimensione del filtro e valore visualizzato
        slider_layout = QHBoxLayout()  # Layout orizzontale per slider e valore
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(5)
        self.slider.valueChanged.connect(self.update_slider_label)  # Aggiorna l'etichetta ad ogni cambiamento di valore
        slider_layout.addWidget(self.slider)

        # Etichetta per visualizzare il valore corrente dello slider
        self.slider_label = QLabel(f"Valore: {self.slider.value()}", self)
        self.slider_label.setFont(large_font)
        slider_layout.addWidget(self.slider_label)
        self.layout.addLayout(slider_layout)

        # Aree di visualizzazione delle immagini (originale e restaurata)
        self.original_label = QLabel(self)
        self.restored_label = QLabel(self)

        # Politiche di ridimensionamento per le immagini
        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.restored_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Aggiungiamo le etichette al layout delle immagini affiancate
        self.image_layout.addWidget(self.original_label)
        self.image_layout.addWidget(self.restored_label)

        # Aggiungiamo il layout delle immagini al layout principale
        self.layout.addLayout(self.image_layout)

        # Spaziatore per migliorare l'estetica
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Lista per i filtri applicati
        self.filter_list = QListWidget(self)
        self.filter_list.setFont(large_font)
        self.filter_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.filter_list)

        # Bottone per rimuovere il filtro selezionato con icona
        self.remove_button = QPushButton('Rimuovi Filtro Selezionato', self)
        self.remove_button.setFont(large_font)
        self.remove_button.setIcon(QIcon('remove_icon.png'))  # Assumi che tu abbia un'icona chiamata remove_icon.png
        self.remove_button.setIconSize(QSize(32, 32))
        self.remove_button.clicked.connect(self.remove_filter)
        self.layout.addWidget(self.remove_button)

        # Widget principale
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica Immagine", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if fileName:
            # Prima rimuoviamo le immagini precedenti
            self.original_label.clear()  # Rimuove l'immagine precedente dall'area originale
            self.restored_label.clear()  # Rimuove l'immagine precedente dall'area restaurata

            # Carica la nuova immagine
            self.image = cv2.imread(fileName)

            # Controlla se l'immagine è stata caricata correttamente
            if self.image is None:
                print("Errore: Immagine non caricata correttamente")
                return

            # Convertiamo l'immagine in RGB per la visualizzazione
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(image_rgb, self.original_label)

            # Resetta la lista dei filtri quando si carica una nuova immagine
            self.reset_filters()

    def apply_filter(self):
        selected_filter = self.filter_combo.currentText()

        if selected_filter == "Filtro Mediano":
            ksize = self.slider.value()
            self.applied_filters.append(('Filtro Mediano', ksize))  # Aggiunge il filtro alla lista
        elif selected_filter == "Filtro Media Aritmetica":
            kernel_size = self.slider.value()  # Dimensione del kernel per la media aritmetica
            self.applied_filters.append(('Filtro Media Aritmetica', kernel_size))  # Aggiunge il filtro alla lista

        self.update_filter_list()  # Aggiorna la lista visibile dei filtri
        self.apply_all_filters()  # Applica tutti i filtri e aggiorna l'immagine

    def apply_all_filters(self):
        """Applica tutti i filtri sulla base dell'immagine originale"""
        temp_image = self.image.copy()  # Copia dell'immagine originale

        for filter_name, param in self.applied_filters:
            if filter_name == "Filtro Mediano":
                temp_image = median_filter(temp_image, param)
            elif filter_name == "Filtro Media Aritmetica":
                temp_image = mean_filter(temp_image, param)

        # Visualizza l'immagine filtrata
        image_rgb = cv2.cvtColor(temp_image, cv2.COLOR_BGR2RGB)
        self.display_image(image_rgb, self.restored_label)

    def update_filter_list(self):
        """Aggiorna la lista visualizzata dei filtri applicati"""
        self.filter_list.clear()
        for filter_name, param in self.applied_filters:
            self.filter_list.addItem(f"{filter_name} (parametro: {param})")

    def remove_filter(self):
        """Rimuove il filtro selezionato dalla lista"""
        selected_items = self.filter_list.selectedItems()
        if not selected_items:
            return

        # Rimuove il filtro selezionato dalla lista interna
        for item in selected_items:
            row = self.filter_list.row(item)
            self.applied_filters.pop(row)

        self.update_filter_list()  # Aggiorna la lista visuale
        self.apply_all_filters()  # Riapplica i filtri rimasti

    def reset_filters(self):
        """Resetta la lista dei filtri applicati"""
        self.applied_filters = []
        self.filter_list.clear()

    def display_image(self, image, label):
        """Visualizza l'immagine su QLabel ridimensionandola alla grandezza della QLabel"""
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Ridimensiona l'immagine per adattarla all'etichetta mantenendo il rapporto d'aspetto
        pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def update_slider_label(self):
        """Aggiorna l'etichetta per mostrare il valore corrente dello slider"""
        self.slider_label.setText(f"Valore: {self.slider.value()}")
