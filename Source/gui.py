from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QLabel, QWidget, QFileDialog, QApplication, QHBoxLayout, \
    QListWidget, QListWidgetItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt, QSize
from filter_worker import FilterWorker
from filter_dialogs import HomomorphicFilterDialog, MedianFilterDialog, ShockFilterDialog, MeanFilterDialog
from image_manager import load_image, convert_to_rgb, display_image, show_image_zoomed, save_image
from utils import save_filter_configuration, load_filter_configuration
from filter_item_widget import FilterItemWidget
import sys


class ImageRestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image = None
        self.restored_image = None
        self.applied_filters = []  # Lista dei filtri applicati
        self.undo_stack = []  # Stack per undo dei filtri
        self.redo_stack = []  # Stack per redo dei filtri

        self.initUI()

    def initUI(self):
        # Impostazioni base della finestra (occupare tutto lo schermo)
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setFixedSize(screen.width(), screen.height())  # Fissa la dimensione della finestra
        self.setWindowTitle('Restauro Immagini')

        # Layout principale
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Label per mostrare l'immagine originale e restaurata
        self.original_label = QLabel('Immagine originale', self)
        self.original_label.setAlignment(Qt.AlignCenter)
        self.restored_label = QLabel('Immagine restaurata', self)
        self.restored_label.setAlignment(Qt.AlignCenter)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.restored_label)
        self.layout.addLayout(image_layout)

        # Aggiungere i pulsanti Undo e Redo
        button_layout = QHBoxLayout()

        self.undo_button = QPushButton('←', self)
        self.undo_button.setFont(QFont("Arial", 14))
        self.undo_button.clicked.connect(self.undo_filter)
        button_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton('→', self)
        self.redo_button.setFont(QFont("Arial", 14))
        self.redo_button.clicked.connect(self.redo_filter)
        button_layout.addWidget(self.redo_button)

        self.layout.addLayout(button_layout)

        # Lista dei filtri applicati (spostata in basso e ridotta)
        self.filter_list = QListWidget(self)
        self.filter_list.setFont(QFont("Arial", 10))
        self.filter_list.setMaximumHeight(150)  # Altezza ridotta
        self.filter_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Dimensione fissa

        # Aggiungi la lista dei filtri in basso
        self.layout.addWidget(self.filter_list)

        # Barra dei menu
        menubar = self.menuBar()

        # Menu File
        file_menu = menubar.addMenu('File')

        # Azione per caricare l'immagine
        load_action = QAction('Carica immagine', self)
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)

        # Azione per salvare l'immagine restaurata
        save_image_action = QAction('Salva immagine', self)
        save_image_action.triggered.connect(self.save_restored_image)
        file_menu.addAction(save_image_action)

        # Azioni per salvare e caricare la configurazione dei filtri
        save_action = QAction('Salva configurazione filtri', self)
        save_action.triggered.connect(self.save_filter_configuration_action)
        file_menu.addAction(save_action)

        load_action = QAction('Carica configurazione filtri', self)
        load_action.triggered.connect(self.load_filter_configuration_action)
        file_menu.addAction(load_action)

        # Menu Filtri
        filter_menu = menubar.addMenu('Filtri')

        # Aggiungere i filtri al menu
        filter_menu.addAction('Filtro Mediano', self.show_median_filter_dialog)
        filter_menu.addAction('Filtro Media Aritmetica', self.show_mean_filter_dialog)
        filter_menu.addAction('Filtro Shock', self.show_shock_filter_dialog)
        filter_menu.addAction('Filtro Homomorphic', self.show_homomorphic_filter_dialog)

        # Configurare le scorciatoie da tastiera per Undo e Redo
        undo_shortcut = QAction('Undo', self)
        undo_shortcut.setShortcut(QKeySequence("Ctrl+Z"))
        undo_shortcut.triggered.connect(self.undo_filter)
        self.addAction(undo_shortcut)

        redo_shortcut = QAction('Redo', self)
        redo_shortcut.setShortcut(QKeySequence("Ctrl+Shift+Z"))
        redo_shortcut.triggered.connect(self.redo_filter)
        self.addAction(redo_shortcut)

    # Funzioni per gestire Undo e Redo
    def undo_filter(self):
        if not self.applied_filters:
            return  # Nessun filtro da annullare
        last_filter = self.applied_filters.pop()  # Rimuovi l'ultimo filtro applicato
        self.undo_stack.append(last_filter)  # Aggiungi allo stack di undo
        self.update_filter_list()  # Aggiorna la lista dei filtri
        self.apply_all_filters()  # Ricalcola i filtri rimasti

    def redo_filter(self):
        if not self.undo_stack:
            return  # Nessun filtro da ripristinare
        last_undo = self.undo_stack.pop()  # Ripristina l'ultimo filtro annullato
        self.applied_filters.append(last_undo)  # Riapplica il filtro
        self.update_filter_list()  # Aggiorna la lista dei filtri
        self.apply_all_filters()  # Ricalcola i filtri applicati

    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica Immagine", "", "Image Files (*.png *.jpg *.jpeg)",
                                                  options=options)
        if fileName:
            self.image = load_image(fileName)
            if self.image is not None:
                image_rgb = convert_to_rgb(self.image)
                display_image(image_rgb, self.original_label)
                self.restored_label.clear()
                self.reset_filters()

    def save_restored_image(self):
        if self.restored_image is not None:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Salva Immagine Restaurata", "SavedImages/",
                                                      "Image Files (*.png *.jpg *.jpeg)", options=options)
            if fileName:
                save_image(self.restored_image, fileName)

    def save_filter_configuration_action(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Salva Configurazione Filtri", "FilterConfig/",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            save_filter_configuration(self.applied_filters, fileName)

    def load_filter_configuration_action(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica Configurazione Filtri", "FilterConfig/",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            filters = load_filter_configuration(fileName)
            if filters is not None:
                self.applied_filters = filters
                self.apply_all_filters()

    # Funzioni per aprire le finestre di dialogo dei filtri
    def show_median_filter_dialog(self):
        dialog = MedianFilterDialog(self, self.apply_median_filter)
        dialog.exec_()

    def show_mean_filter_dialog(self):
        dialog = MeanFilterDialog(self, self.apply_mean_filter)
        dialog.exec_()

    def show_shock_filter_dialog(self):
        dialog = ShockFilterDialog(self, self.apply_shock_filter)
        dialog.exec_()

    def show_homomorphic_filter_dialog(self):
        dialog = HomomorphicFilterDialog(self, self.apply_homomorphic_filter)
        dialog.exec_()

    # Funzioni per applicare i filtri
    def apply_median_filter(self, ksize):
        self.applied_filters.append(('Filtro Mediano', ksize))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_mean_filter(self, kernel_size):
        self.applied_filters.append(('Filtro Media Aritmetica', kernel_size))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_shock_filter(self, iterations):
        self.applied_filters.append(('Filtro Shock', iterations))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_homomorphic_filter(self, low, high, cutoff):
        self.applied_filters.append(('Filtro Homomorphic', {'low': low, 'high': high, 'cutoff': cutoff}))
        self.update_filter_list()
        self.apply_all_filters()

    # Funzione per aggiornare la lista dei filtri applicati
    def update_filter_list(self):
        self.filter_list.clear()
        for index, (filter_name, param) in enumerate(self.applied_filters):
            item_widget = FilterItemWidget(filter_name, param, self.create_remove_callback(index))
            list_item = QListWidgetItem(self.filter_list)
            list_item.setSizeHint(item_widget.sizeHint())
            self.filter_list.addItem(list_item)
            self.filter_list.setItemWidget(list_item, item_widget)

    def create_remove_callback(self, index):
        return lambda: self.remove_filter(index)

    # Funzione per rimuovere un filtro dalla lista
    def remove_filter(self, index):
        self.applied_filters.pop(index)
        self.update_filter_list()
        self.apply_all_filters()

    # Funzione per resettare i filtri
    def reset_filters(self):
        self.applied_filters = []
        self.filter_list.clear()

    # Funzione per applicare tutti i filtri all'immagine
    def apply_all_filters(self):
        if self.image is not None:
            if hasattr(self, 'worker') and self.worker.isRunning():
                self.worker.stop()
                self.worker.wait()

            # Avvia un nuovo worker per applicare i filtri
            self.worker = FilterWorker(self.image, self.applied_filters)
            self.worker.filter_applied.connect(self.on_filter_applied)
            self.worker.start()

    def on_filter_applied(self, result_image):
        self.restored_image = result_image
        image_rgb = convert_to_rgb(result_image)
        display_image(image_rgb, self.restored_label)
