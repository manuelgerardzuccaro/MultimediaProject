from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QWidget, QListWidget, QSizePolicy, QSpacerItem, QMenuBar, QAction, QListWidgetItem
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication
from filters import median_filter, mean_filter  # Importa i filtri dal file filters.py

class FilterItemWidget(QWidget):
    def __init__(self, filter_name, param, remove_callback):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Etichetta con il nome del filtro e il parametro
        self.label = QLabel(f"{filter_name} (parametro: {param})", self)
        self.layout.addWidget(self.label)

        # Pulsante per rimuovere il filtro
        self.remove_button = QPushButton("X", self)
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.clicked.connect(remove_callback)  # Collegare la funzione per rimuovere il filtro
        self.layout.addWidget(self.remove_button)

class ImageRestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.applied_filters = []  # Lista per memorizzare i filtri applicati

    def initUI(self):
        # Ottieni la risoluzione dello schermo
        screen_resolution = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

        # Imposta la finestra a schermo intero e blocca il ridimensionamento
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setFixedSize(screen_width, screen_height)
        self.setWindowTitle('Restauro Immagini - Riduzione Rumore')
        self.showMaximized()

        # Barra dei menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # Aggiungi azione "Carica Immagine" nel menu
        load_action = QAction('Carica Immagine', self)
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)

        # Layout principale verticale
        main_layout = QVBoxLayout()

        # --- Sezione superiore con i controlli dei filtri ---
        controls_layout = QHBoxLayout()
        large_font = QFont("Arial", 12)  # Font size increased

        # Menu a tendina per la selezione del filtro
        self.filter_combo = QComboBox(self)
        self.filter_combo.setFont(large_font)
        self.filter_combo.addItems(["Filtro Mediano", "Filtro Media Aritmetica"])
        controls_layout.addWidget(self.filter_combo)

        # Slider per la dimensione del filtro
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

        controls_layout.addLayout(slider_layout)

        # Bottone per applicare il filtro
        self.apply_button = QPushButton('Applica Filtro', self)
        self.apply_button.setFont(large_font)
        self.apply_button.setIcon(QIcon('apply_icon.png'))  # Assumi che tu abbia un'icona chiamata apply_icon.png
        self.apply_button.setIconSize(QSize(32, 32))
        self.apply_button.clicked.connect(self.apply_filter)
        controls_layout.addWidget(self.apply_button)

        main_layout.addLayout(controls_layout)

        # --- Sezione centrale con le immagini disposte in orizzontale ---
        image_layout = QHBoxLayout()

        # Aree di visualizzazione delle immagini (originale e restaurata)
        self.original_label = QLabel(self)
        self.restored_label = QLabel(self)

        # Politiche di ridimensionamento per le immagini
        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.restored_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Centratura delle immagini
        self.original_label.setAlignment(Qt.AlignCenter)
        self.restored_label.setAlignment(Qt.AlignCenter)

        # Aggiungiamo le etichette al layout delle immagini
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.restored_label)

        main_layout.addLayout(image_layout)

        # --- Sezione inferiore con la lista dei filtri applicati ---
        self.filter_list = QListWidget(self)
        self.filter_list.setFont(large_font)
        self.filter_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.filter_list)

        # Widget principale
        container = QWidget()
        container.setLayout(main_layout)
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
        for index, (filter_name, param) in enumerate(self.applied_filters):
            # Crea un widget personalizzato con il nome del filtro e il pulsante di rimozione
            item_widget = FilterItemWidget(filter_name, param, lambda i=index: self.remove_filter(i))
            list_item = QListWidgetItem(self.filter_list)
            list_item.setSizeHint(item_widget.sizeHint())

            # Aggiungi il widget alla lista
            self.filter_list.addItem(list_item)
            self.filter_list.setItemWidget(list_item, item_widget)

    def remove_filter(self, index):
        """Rimuove il filtro selezionato dalla lista interna"""
        self.applied_filters.pop(index)
        self.update_filter_list()  # Aggiorna la lista visiva
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
