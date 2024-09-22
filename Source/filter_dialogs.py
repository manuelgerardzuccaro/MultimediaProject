from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QRadioButton


class HomomorphicFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Homomorphic")

        layout = QVBoxLayout(self)

        # Slider per il parametro "Low"
        self.low_slider = QSlider(Qt.Horizontal)
        self.low_slider.setMinimum(1)
        self.low_slider.setMaximum(10)
        self.low_slider.setValue(5)
        self.low_label = QLabel(f"Low: {self.low_slider.value() / 10}", self)
        self.low_slider.valueChanged.connect(lambda: self.low_label.setText(f"Low: {self.low_slider.value() / 10}"))

        # Slider per il parametro "High"
        self.high_slider = QSlider(Qt.Horizontal)
        self.high_slider.setMinimum(10)
        self.high_slider.setMaximum(20)
        self.high_slider.setValue(15)
        self.high_label = QLabel(f"High: {self.high_slider.value() / 10}", self)
        self.high_slider.valueChanged.connect(lambda: self.high_label.setText(f"High: {self.high_slider.value() / 10}"))

        # Slider per il parametro "Cutoff"
        self.cutoff_slider = QSlider(Qt.Horizontal)
        self.cutoff_slider.setMinimum(10)
        self.cutoff_slider.setMaximum(100)
        self.cutoff_slider.setValue(30)
        self.cutoff_label = QLabel(f"Cutoff: {self.cutoff_slider.value()}", self)
        self.cutoff_slider.valueChanged.connect(
            lambda: self.cutoff_label.setText(f"Cutoff: {self.cutoff_slider.value()}"))

        # Aggiungi gli slider al layout
        layout.addWidget(self.low_label)
        layout.addWidget(self.low_slider)
        layout.addWidget(self.high_label)
        layout.addWidget(self.high_slider)
        layout.addWidget(self.cutoff_label)
        layout.addWidget(self.cutoff_slider)

        # Pulsante Applica
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        # Pulsante Cancella
        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        low = self.low_slider.value() / 10.0
        high = self.high_slider.value() / 10.0
        cutoff = self.cutoff_slider.value()
        self.apply_callback(low, high, cutoff)  # Callback per applicare il filtro
        self.close()


# Simile al Filtro Homomorphic, possiamo definire altre finestre di dialogo, ad esempio:
class MedianFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Mediano")

        layout = QVBoxLayout(self)

        # Slider per il parametro "ksize"
        self.ksize_slider = QSlider(Qt.Horizontal)
        self.ksize_slider.setMinimum(1)
        self.ksize_slider.setMaximum(11)
        self.ksize_slider.setValue(3)
        self.ksize_label = QLabel(f"Kernel size: {self.ksize_slider.value()}", self)
        self.ksize_slider.valueChanged.connect(
            lambda: self.ksize_label.setText(f"Kernel size: {self.ksize_slider.value()}"))

        # Aggiungi lo slider al layout
        layout.addWidget(self.ksize_label)
        layout.addWidget(self.ksize_slider)

        # Pulsante Applica
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        # Pulsante Cancella
        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        ksize = self.ksize_slider.value()
        self.apply_callback(ksize)  # Callback per applicare il filtro
        self.close()


# Dialogo per il filtro Shock
class ShockFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Shock")

        # Layout principale
        layout = QVBoxLayout(self)

        # Slider per le iterazioni del filtro Shock
        self.iterations_slider = QSlider(Qt.Horizontal)
        self.iterations_slider.setMinimum(1)  # Minimo 1 iterazione
        self.iterations_slider.setMaximum(100)  # Massimo 100 iterazioni
        self.iterations_slider.setValue(10)  # Valore iniziale
        self.iterations_label = QLabel(f"Iterazioni: {self.iterations_slider.value()}", self)
        self.iterations_slider.valueChanged.connect(
            lambda: self.iterations_label.setText(f"Iterazioni: {self.iterations_slider.value()}"))

        # Aggiungi lo slider al layout
        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_slider)

        # Layout per i pulsanti "Applica" e "Cancella"
        button_layout = QHBoxLayout()

        # Pulsante Applica
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        # Pulsante Cancella
        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        # Aggiungi il layout dei pulsanti al layout principale
        layout.addLayout(button_layout)

        # Callback per l'applicazione del filtro
        self.apply_callback = apply_callback

    def apply_filter(self):
        iterations = self.iterations_slider.value()
        self.apply_callback(iterations)  # Passa il numero di iterazioni al callback
        self.close()


# Dialogo per il filtro Media Aritmetica
class MeanFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Media Aritmetica")

        # Layout principale
        layout = QVBoxLayout(self)

        # Slider per la dimensione del kernel
        self.kernel_size_slider = QSlider(Qt.Horizontal)
        self.kernel_size_slider.setMinimum(3)  # Minimo kernel 3x3
        self.kernel_size_slider.setMaximum(15)  # Massimo kernel 15x15
        self.kernel_size_slider.setValue(3)  # Valore iniziale
        self.kernel_size_label = QLabel(f"Kernel Size: {self.kernel_size_slider.value()}", self)
        self.kernel_size_slider.valueChanged.connect(
            lambda: self.kernel_size_label.setText(f"Kernel Size: {self.kernel_size_slider.value()}"))

        # Aggiungi lo slider al layout
        layout.addWidget(self.kernel_size_label)
        layout.addWidget(self.kernel_size_slider)

        # Layout per i pulsanti "Applica" e "Cancella"
        button_layout = QHBoxLayout()

        # Pulsante Applica
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        # Pulsante Cancella
        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        # Aggiungi il layout dei pulsanti al layout principale
        layout.addLayout(button_layout)

        # Callback per l'applicazione del filtro
        self.apply_callback = apply_callback

    def apply_filter(self):
        kernel_size = self.kernel_size_slider.value()
        self.apply_callback(kernel_size)  # Passa la dimensione del kernel al callback
        self.close()


class AnisotropicDiffusionDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Diffusione Anisotropica")

        layout = QVBoxLayout(self)

        # Slider per il numero di iterazioni
        self.iterations_slider = QSlider(Qt.Horizontal)
        self.iterations_slider.setMinimum(1)
        self.iterations_slider.setMaximum(50)
        self.iterations_slider.setValue(10)
        self.iterations_label = QLabel(f"Iterazioni: {self.iterations_slider.value()}", self)
        self.iterations_slider.valueChanged.connect(
            lambda: self.iterations_label.setText(f"Iterazioni: {self.iterations_slider.value()}"))

        # Slider per il parametro k
        self.k_slider = QSlider(Qt.Horizontal)
        self.k_slider.setMinimum(5)
        self.k_slider.setMaximum(100)
        self.k_slider.setValue(15)
        self.k_label = QLabel(f"K: {self.k_slider.value()}", self)
        self.k_slider.valueChanged.connect(lambda: self.k_label.setText(f"K: {self.k_slider.value()}"))

        # Slider per il parametro gamma
        self.gamma_slider = QSlider(Qt.Horizontal)
        self.gamma_slider.setMinimum(1)
        self.gamma_slider.setMaximum(100)
        self.gamma_slider.setValue(10)
        self.gamma_label = QLabel(f"Gamma: {self.gamma_slider.value() / 100.0}", self)
        self.gamma_slider.valueChanged.connect(
            lambda: self.gamma_label.setText(f"Gamma: {self.gamma_slider.value() / 100.0}"))

        # RadioButton per la scelta dell'opzione di diffusione
        self.option1_radio = QRadioButton("Opzione 1 (esponenziale)")
        self.option2_radio = QRadioButton("Opzione 2 (razionale)")
        self.option1_radio.setChecked(True)

        # Aggiungi gli elementi al layout
        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_slider)
        layout.addWidget(self.k_label)
        layout.addWidget(self.k_slider)
        layout.addWidget(self.gamma_label)
        layout.addWidget(self.gamma_slider)
        layout.addWidget(self.option1_radio)
        layout.addWidget(self.option2_radio)

        # Pulsante Applica
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        # Pulsante Cancella
        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        iterations = self.iterations_slider.value()
        k = self.k_slider.value()
        gamma = self.gamma_slider.value() / 100.0
        option = 1 if self.option1_radio.isChecked() else 2
        self.apply_callback(iterations, k, gamma, option)
        self.close()
