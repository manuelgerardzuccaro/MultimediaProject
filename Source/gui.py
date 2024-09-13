from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QLabel, QListWidget, QWidget, \
    QListWidgetItem, QAction, QFileDialog, QPushButton, QSizePolicy, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from filter_item_widget import FilterItemWidget
from filter_worker import FilterWorker
from utils import save_filter_configuration, load_filter_configuration, save_image
from image_manager import load_image, convert_to_rgb, display_image

class ImageRestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.applied_filters = []  # Lista dei filtri applicati
        self.undo_stack = []  # Stack per gestire le operazioni di undo
        self.redo_stack = []  # Stack per gestire le operazioni di redo

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
        load_action = QAction('Carica immagine', self)
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)

        save_image_action = QAction('Salva immagine', self)
        save_image_action.triggered.connect(self.save_restored_image)
        file_menu.addAction(save_image_action)

        save_action = QAction('Salva configurazione filtri', self)
        save_action.triggered.connect(self.save_filter_configuration_action)
        file_menu.addAction(save_action)

        load_action = QAction('Carica configurazione filtri', self)
        load_action.triggered.connect(self.load_filter_configuration_action)
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

        # Bottone Undo
        self.undo_button = QPushButton('Undo', self)
        self.undo_button.setFont(large_font)
        self.undo_button.clicked.connect(self.undo_filter)

        controls_layout.addWidget(self.undo_button)

        # Bottone Redo
        self.redo_button = QPushButton('Redo', self)
        self.redo_button.setFont(large_font)
        self.redo_button.clicked.connect(self.redo_filter)

        controls_layout.addWidget(self.redo_button)

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

    def undo_filter(self):
        if not self.applied_filters:
            return  # Nessun filtro da annullare

        # Sposta l'ultimo filtro nello stack di redo
        last_filter = self.applied_filters.pop()
        self.undo_stack.append(last_filter)

        # Applica nuovamente tutti i filtri rimanenti
        self.update_filter_list()
        self.apply_all_filters()

    def redo_filter(self):
        if not self.undo_stack:
            return  # Nessun filtro da ripristinare

        # Ripristina l'ultimo filtro dallo stack di undo
        last_undo = self.undo_stack.pop()
        self.applied_filters.append(last_undo)

        # Aggiorna la lista e riapplica i filtri
        self.update_filter_list()
        self.apply_all_filters()

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

    def save_restored_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Salva Immagine Restaurata",
            "SavedImages/",  # Cartella predefinita
            "Image Files (*.png *.jpg *.jpeg)",
            options=options
        )
        if fileName:
            save_image(self.restored_image, fileName)  # Funzione save_image già presente in utils


    def save_filter_configuration_action(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Salva Configurazione Filtri",
            "FilterConfig/",  # Cartella predefinita
            "JSON Files (*.json)",
            options=options
        )
        if fileName:
            save_filter_configuration(self.applied_filters, fileName)

    def load_filter_configuration_action(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Carica Configurazione Filtri",
            "FilterConfig/",  # Cartella predefinita
            "JSON Files (*.json)",
            options=options
        )
        if fileName:
            filters = load_filter_configuration(fileName)
            if filters is not None:
                self.applied_filters = filters
                self.update_filter_list()
                self.apply_all_filters()

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
        if hasattr(self, 'worker'):
            self.worker.terminate()  # Termina eventuali thread precedenti

        # Crea un nuovo worker e collega il segnale
        self.worker = FilterWorker(self.image, self.applied_filters)
        self.worker.filter_applied.connect(self.on_filter_applied)
        self.worker.start()

    def on_filter_applied(self, result_image):
        self.restored_image = result_image  # Salva l'immagine restaurata
        image_rgb = convert_to_rgb(result_image)
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
