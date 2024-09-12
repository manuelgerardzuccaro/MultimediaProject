from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QLabel, QListWidget, QWidget, \
    QListWidgetItem, QAction, QFileDialog, QPushButton, QSizePolicy, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from filter_item_widget import FilterItemWidget
from filters import median_filter, mean_filter
from image_manager import load_image, convert_to_rgb, display_image

class ImageRestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.applied_filters = []  # Lista per memorizzare i filtri applicati

    def initUI(self):
        # Imposta il font globale tramite fogli di stile
        self.setup_stylesheet()

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
        large_font = QFont("Arial", 12)

        # Menu a tendina per la selezione del filtro
        self.filter_combo = QComboBox(self)
        self.filter_combo.setFont(large_font)
        self.filter_combo.addItems(["Filtro Mediano", "Filtro Media Aritmetica"])
        controls_layout.addWidget(self.filter_combo)

        # Slider per la dimensione del filtro
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(5)
        self.slider.valueChanged.connect(self.update_slider_label)
        slider_layout.addWidget(self.slider)

        # Etichetta per visualizzare il valore corrente dello slider
        self.slider_label = QLabel(f"Valore: {self.slider.value()}", self)
        self.slider_label.setFont(large_font)
        slider_layout.addWidget(self.slider_label)

        controls_layout.addLayout(slider_layout)

        # Bottone per applicare il filtro
        self.apply_button = QPushButton('Applica Filtro', self)
        self.apply_button.setFont(large_font)
        self.apply_button.setIcon(QIcon('apply_icon.png'))
        self.apply_button.setIconSize(QSize(32, 32))
        self.apply_button.clicked.connect(self.apply_filter)
        controls_layout.addWidget(self.apply_button)

        main_layout.addLayout(controls_layout)

        # --- Sezione centrale con le immagini disposte in orizzontale ---
        image_layout = QHBoxLayout()

        self.original_label = QLabel(self)
        self.restored_label = QLabel(self)

        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.restored_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.original_label.setAlignment(Qt.AlignCenter)
        self.restored_label.setAlignment(Qt.AlignCenter)

        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.restored_label)

        main_layout.addLayout(image_layout)

        # --- Sezione inferiore con la lista dei filtri applicati ---
        self.filter_list = QListWidget(self)
        self.filter_list.setFont(large_font)

        # Imposta l'altezza massima della lista dei filtri applicati
        self.filter_list.setMaximumHeight(350)  # Imposta una dimensione massima per la lista

        # Imposta una politica di ridimensionamento espansiva
        self.filter_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Aggiungi la lista al layout principale
        main_layout.addWidget(self.filter_list)

        # Widget principale
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_stylesheet(self):
        """Imposta il foglio di stile dell'interfaccia"""
        self.setStyleSheet("""
            QMenuBar {
                font-size: 18px;
            }
            QMenu {
                font-size: 18px;
            }
            QLabel {
                font-size: 20px;
            }
            QPushButton {
                font-size: 18px;
            }
            QComboBox {
                font-size: 18px;
            }
            QListWidget {
                font-size: 18px;
            }
            QSlider {
                font-size: 18px;
            }
        """)

    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica Immagine", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if fileName:
            self.image = load_image(fileName)

            # Se l'immagine è caricata correttamente, visualizzala immediatamente
            if self.image is not None:
                image_rgb = convert_to_rgb(self.image)
                display_image(image_rgb, self.original_label)  # Visualizza subito l'immagine originale

                # Cancella l'immagine restaurata, se esiste
                self.restored_label.clear()

                # Resetta la lista dei filtri quando si carica una nuova immagine
                self.reset_filters()

    def apply_filter(self):
        selected_filter = self.filter_combo.currentText()

        if selected_filter == "Filtro Mediano":
            ksize = self.slider.value()
            self.applied_filters.append(('Filtro Mediano', ksize))
        elif selected_filter == "Filtro Media Aritmetica":
            kernel_size = self.slider.value()
            self.applied_filters.append(('Filtro Media Aritmetica', kernel_size))

        self.update_filter_list()
        self.apply_all_filters()

    def apply_all_filters(self):
        temp_image = self.image.copy()

        for filter_name, param in self.applied_filters:
            if filter_name == "Filtro Mediano":
                temp_image = median_filter(temp_image, param)
            elif filter_name == "Filtro Media Aritmetica":
                temp_image = mean_filter(temp_image, param)

        image_rgb = convert_to_rgb(temp_image)
        display_image(image_rgb, self.restored_label)

    def update_filter_list(self):
        self.filter_list.clear()
        for index, (filter_name, param) in enumerate(self.applied_filters):
            item_widget = FilterItemWidget(filter_name, param, lambda i=index: self.remove_filter(i))
            list_item = QListWidgetItem(self.filter_list)
            list_item.setSizeHint(item_widget.sizeHint())

            self.filter_list.addItem(list_item)
            self.filter_list.setItemWidget(list_item, item_widget)

    def remove_filter(self, index):
        self.applied_filters.pop(index)
        self.update_filter_list()
        self.apply_all_filters()

    def reset_filters(self):
        self.applied_filters = []
        self.filter_list.clear()

    def update_slider_label(self):
        self.slider_label.setText(f"Valore: {self.slider.value()}")
