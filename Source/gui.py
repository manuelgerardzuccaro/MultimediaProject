import csv
import os

import cv2
from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QLabel, QWidget, QFileDialog, QApplication, QHBoxLayout, \
    QListWidget, QListWidgetItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt, QSize
from filter_worker import FilterWorker
from filter_dialogs import *
from image_manager import load_image, convert_to_rgb, display_image, show_image_zoomed, save_image
from utils import save_filter_configuration, load_filter_configuration, calculate_psnr, calculate_mse, calculate_ssim, \
    is_grayscale
from filter_item_widget import FilterItemWidget
import sys


class ImageRestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image = None
        self.restored_image = None
        self.applied_filters = []  # lista dei filtri applicati
        self.undo_stack = []  # stack per undo dei filtri
        self.redo_stack = []  # stack per redo dei filtri

        self.initUI()

    def initUI(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setFixedSize(screen.width(), screen.height())
        self.setWindowTitle('Restauro Immagini')

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.original_label = QLabel('Immagine originale', self)
        self.original_label.setAlignment(Qt.AlignCenter)
        self.restored_label = QLabel('Immagine restaurata', self)
        self.restored_label.setAlignment(Qt.AlignCenter)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.restored_label)
        self.layout.addLayout(image_layout)

        # pulsanti Undo e Redo
        button_layout = QHBoxLayout()

        undo_button = QPushButton('←', self)
        undo_button.setFont(QFont("Arial", 14))
        undo_button.clicked.connect(self.undo_filter)
        button_layout.addWidget(undo_button)

        redo_button = QPushButton('→', self)
        redo_button.setFont(QFont("Arial", 14))
        redo_button.clicked.connect(self.redo_filter)
        button_layout.addWidget(redo_button)

        self.layout.addLayout(button_layout)

        # lista filtri applicati
        self.filter_list = QListWidget(self)
        self.filter_list.setFont(QFont("Arial", 10))
        self.filter_list.setMaximumHeight(150)
        self.filter_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.filter_list)

        # barra menu
        menubar = self.menuBar()

        # barra menu - file
        file_menu = menubar.addMenu('File')

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

        # barra menu - filtri
        filter_menu = menubar.addMenu('Filtri')

        filter_menu.addAction('Filtro Mediano', self.show_median_filter_dialog)
        filter_menu.addAction('Filtro MedianBlur', self.show_median_blur_filter_dialog)
        filter_menu.addAction('Filtro Media Aritmetica', self.show_mean_filter_dialog)
        filter_menu.addAction('Filtro Media Geometrica', self.show_geometric_mean_filter_dialog)
        filter_menu.addAction('Filtro Media Geometrica Logaritmica', self.show_log_geometric_mean_filter_dialog)
        filter_menu.addAction('Filtro Gaussiano', self.show_gaussian_filter_dialog)
        filter_menu.addAction('Filtro Contra-Harmonic Mean', self.show_contra_harmonic_mean_filter_dialog)
        filter_menu.addAction('Filtro Notch', self.show_notch_filter_dialog)
        filter_menu.addAction('Filtro Shock', self.show_shock_filter_dialog)
        filter_menu.addAction('Filtro Homomorphic', self.show_homomorphic_filter_dialog)
        filter_menu.addAction('Filtro Diffusione Anisotropica', self.show_anisotropic_diffusion_dialog)
        filter_menu.addAction('Deconvoluzione ℓ1-TV', self.show_l1_tv_deconvolution_dialog)
        filter_menu.addAction('Deconvoluzione Wiener', self.show_wiener_filter_dialog)

        # barra menu - rumori
        noise_menu = menubar.addMenu('Rumori')

        noise_menu.addAction('Rumore Gaussiano', self.apply_gaussian_noise)
        noise_menu.addAction('Rumore Sale e Pepe', self.apply_salt_pepper_noise)
        noise_menu.addAction('Rumore Uniforme', self.apply_uniform_noise)
        noise_menu.addAction('Rumore Grana della Pellicola', self.apply_film_grain_noise)
        noise_menu.addAction('Rumore Periodico', self.apply_periodic_noise)

        # shortcut Undo e Redo
        undo_shortcut = QAction('Undo', self)
        undo_shortcut.setShortcut(QKeySequence("Ctrl+Z"))
        undo_shortcut.triggered.connect(self.undo_filter)
        self.addAction(undo_shortcut)

        redo_shortcut = QAction('Redo', self)
        redo_shortcut.setShortcut(QKeySequence("Ctrl+Shift+Z"))
        redo_shortcut.triggered.connect(self.redo_filter)
        self.addAction(redo_shortcut)

    def undo_filter(self):
        if not self.applied_filters:
            return
        last_filter = self.applied_filters.pop()
        self.undo_stack.append(last_filter)
        self.update_filter_list()
        self.apply_all_filters()

    def redo_filter(self):
        if not self.undo_stack:
            return
        last_undo = self.undo_stack.pop()
        self.applied_filters.append(last_undo)
        self.update_filter_list()
        self.apply_all_filters()

    def load_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica Immagine", "", "Image Files "
                                                                               "(*.png *.jpg *.jpeg)", options=options)
        if fileName:
            self.image = load_image(fileName)
            self.restored_image = self.image

            if self.image is not None:

                if is_grayscale(self.image):
                    self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

                image_rgb = convert_to_rgb(self.image)
                display_image(image_rgb, self.original_label)
                self.restored_label.clear()
                self.reset_filters()
                display_image(image_rgb, self.restored_label)

    def log_filter_results(self, image_name, filters, restored_image, image_id, csv_filename='risultati.csv'):
        # Converti entrambe le immagini in RGB per garantire che abbiano lo stesso formato
        if len(self.image.shape) == 2:  # Se l'immagine originale è in scala di grigi
            original_image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        else:
            original_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        if len(restored_image.shape) == 2:  # Se l'immagine restaurata è in scala di grigi
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_GRAY2RGB)
        else:
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BGR2RGB)

        # Verifica se le immagini hanno la stessa dimensione; in caso contrario, ridimensiona quella restaurata
        if original_image.shape != restored_image.shape:
            restored_image = cv2.resize(restored_image, (original_image.shape[1], original_image.shape[0]))

        # Calcola il PSNR, MSE e SSIM tra l'immagine originale e quella restaurata
        psnr_value = calculate_psnr(original_image, restored_image)
        mse_value = calculate_mse(original_image, restored_image)
        ssim_value = calculate_ssim(original_image, restored_image)

        # Verifica se il file CSV esiste già
        file_exists = os.path.isfile(csv_filename)

        # Scrive i risultati nel file CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Scrive l'intestazione solo se il file non esiste
            if not file_exists:
                writer.writerow(["ID", "NomeFile", "NomeFiltro", "Parametri", "PSNR", "MSE", "SSIM"])

            # Aggiunge i dati per ciascun filtro applicato
            for filter_name, params in filters:
                # Gestisci il tipo dei parametri
                if isinstance(params, dict):
                    filter_data = "; ".join([f"{key}={value}" for key, value in params.items()])
                else:
                    filter_data = str(params)

                # Scrive la riga con l'ID passato come parametro
                writer.writerow([image_id, image_name, filter_name, filter_data, psnr_value, mse_value, ssim_value])
                print(f"Risultati salvati nel CSV per l'immagine: {image_name}")

    def save_restored_image(self):
        if self.restored_image is not None:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Salva Immagine Restaurata", "SavedImages/",
                                                      "Image Files (*.png *.jpg *.jpeg)", options=options)
            if fileName:
                save_image(self.restored_image, fileName)

                # Genera un nuovo ID solo una volta per questa immagine
                csv_filename = 'risultati.csv'
                file_exists = os.path.isfile(csv_filename)
                image_id = 1  # ID iniziale
                if file_exists:
                    with open(csv_filename, mode='r', newline='') as file:
                        reader = csv.reader(file)
                        next(reader)  # Salta l'intestazione
                        ids = [int(row[0]) for row in reader if row]  # Estrai tutti gli ID esistenti
                        if ids:
                            image_id = max(ids) + 1  # Incrementa l'ID massimo esistente

                # Salva i risultati nel CSV con l'ID univoco
                image_name = fileName.split('/')[-1]  # Estrai il nome dell'immagine dal percorso
                self.log_filter_results(image_name, self.applied_filters, self.restored_image, image_id)

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

    def show_median_filter_dialog(self):
        dialog = MedianFilterDialog(self, self.apply_median_filter)
        dialog.exec_()

    def show_median_blur_filter_dialog(self):
        dialog = MedianFilterDialog(self, self.apply_median_blur_filter)
        dialog.exec_()

    def show_mean_filter_dialog(self):
        dialog = MeanFilterDialog(self, self.apply_mean_filter)
        dialog.exec_()

    def show_geometric_mean_filter_dialog(self):
        dialog = GeometricMeanFilterDialog(self, self.apply_geometric_mean_filter)
        dialog.exec_()

    def show_log_geometric_mean_filter_dialog(self):
        dialog = LogGeometricMeanFilterDialog(self, self.apply_log_geometric_mean_filter)
        dialog.exec_()

    def show_gaussian_filter_dialog(self):
        dialog = GaussianFilterDialog(self, self.apply_gaussian_filter)
        dialog.exec_()

    def show_contra_harmonic_mean_filter_dialog(self):
        dialog = ContraHarmonicMeanFilterDialog(self, self.apply_contra_harmonic_mean_filter)
        dialog.exec_()

    def show_notch_filter_dialog(self):
        dialog = NotchFilterDialog(self, self.apply_notch_filter)
        dialog.exec_()

    def show_shock_filter_dialog(self):
        dialog = ShockFilterDialog(self, self.apply_shock_filter)
        dialog.exec_()

    def show_homomorphic_filter_dialog(self):
        dialog = HomomorphicFilterDialog(self, self.apply_homomorphic_filter)
        dialog.exec_()

    def show_anisotropic_diffusion_dialog(self):
        dialog = AnisotropicDiffusionDialog(self, self.apply_anisotropic_diffusion)
        dialog.exec_()

    def show_l1_tv_deconvolution_dialog(self):
        dialog = L1TVDeconvolutionDialog(self, self.apply_l1_tv_deconvolution)
        dialog.exec_()

    def show_wiener_filter_dialog(self):
        dialog = WienerFilterDialog(self, self.apply_wiener_deconvolution)
        dialog.exec_()

    def apply_median_filter(self, ksize):
        self.applied_filters.append(('Filtro Mediano', ksize))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_median_blur_filter(self, ksize):
        self.applied_filters.append(('Filtro MedianBlur', ksize))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_mean_filter(self, kernel_size):
        self.applied_filters.append(('Filtro Media Aritmetica', kernel_size))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_geometric_mean_filter(self, kernel_size):
        self.applied_filters.append(('Filtro Media Geometrica', kernel_size))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_log_geometric_mean_filter(self, kernel_size):
        self.applied_filters.append(('Filtro Media Geometrica Logaritmica', kernel_size))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_gaussian_filter(self, kernel_size, sigma):
        self.applied_filters.append(('Filtro Gaussiano', {'kernel_size': kernel_size, 'sigma': sigma}))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_contra_harmonic_mean_filter(self, kernel_size, Q):
        self.applied_filters.append(('Filtro Contra-Harmonic Mean', {'kernel_size': kernel_size, 'Q': Q}))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_notch_filter(self, d0, u_k, v_k):
        self.applied_filters.append(('Filtro Notch', {'d0': d0, 'u_k': u_k, 'v_k': v_k}))
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

    def apply_anisotropic_diffusion(self, iterations, k, gamma, option):
        self.applied_filters.append(
            ('Diffusione Anisotropica', {'iterations': iterations, 'k': k, 'gamma': gamma, 'option': option}))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_l1_tv_deconvolution(self, iterations, regularization_weight):
        self.applied_filters.append(
            ('Deconvoluzione ℓ1-TV', {'iterations': iterations, 'regularization_weight': regularization_weight}))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_wiener_deconvolution(self, kernel_size, noise):
        self.applied_filters.append(('Deconvoluzione Wiener', {'kernel_size': kernel_size, 'noise': noise}))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_gaussian_noise(self):
        self.applied_filters.append(('Rumore Gaussiano', None))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_salt_pepper_noise(self):
        self.applied_filters.append(('Rumore Sale e Pepe', None))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_uniform_noise(self):
        self.applied_filters.append(('Rumore Uniforme', None))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_film_grain_noise(self):
        self.applied_filters.append(('Rumore Grana della Pellicola', None))
        self.update_filter_list()
        self.apply_all_filters()

    def apply_periodic_noise(self):
        self.applied_filters.append(('Rumore Periodico', None))
        self.update_filter_list()
        self.apply_all_filters()

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

    def remove_filter(self, index):
        self.applied_filters.pop(index)
        self.update_filter_list()
        self.apply_all_filters()

    def reset_filters(self):
        self.applied_filters = []
        self.filter_list.clear()

    def apply_all_filters(self):
        if self.image is not None:
            if hasattr(self, 'worker') and self.worker.isRunning():
                self.worker.stop()
                self.worker.wait()

            self.worker = FilterWorker(self.image, self.applied_filters)
            self.worker.filter_applied.connect(self.on_filter_applied)
            self.worker.start()

    def on_filter_applied(self, result_image):
        self.restored_image = result_image
        image_rgb = convert_to_rgb(result_image)
        display_image(image_rgb, self.restored_label)
