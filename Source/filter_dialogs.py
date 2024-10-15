from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QRadioButton, QListWidget, \
    QLineEdit, QMessageBox


class HomomorphicFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Homomorphic")

        layout = QVBoxLayout(self)

        self.low_slider = QSlider(Qt.Horizontal)
        self.low_slider.setMinimum(1)
        self.low_slider.setMaximum(10)
        self.low_slider.setValue(5)
        self.low_label = QLabel(f"Low: {self.low_slider.value() / 10}", self)
        self.low_slider.valueChanged.connect(lambda: self.low_label.setText(f"Low: {self.low_slider.value() / 10}"))

        self.high_slider = QSlider(Qt.Horizontal)
        self.high_slider.setMinimum(10)
        self.high_slider.setMaximum(20)
        self.high_slider.setValue(15)
        self.high_label = QLabel(f"High: {self.high_slider.value() / 10}", self)
        self.high_slider.valueChanged.connect(lambda: self.high_label.setText(f"High: {self.high_slider.value() / 10}"))

        self.cutoff_slider = QSlider(Qt.Horizontal)
        self.cutoff_slider.setMinimum(10)
        self.cutoff_slider.setMaximum(100)
        self.cutoff_slider.setValue(30)
        self.cutoff_label = QLabel(f"Cutoff: {self.cutoff_slider.value()}", self)
        self.cutoff_slider.valueChanged.connect(
            lambda: self.cutoff_label.setText(f"Cutoff: {self.cutoff_slider.value()}"))

        layout.addWidget(self.low_label)
        layout.addWidget(self.low_slider)
        layout.addWidget(self.high_label)
        layout.addWidget(self.high_slider)
        layout.addWidget(self.cutoff_label)
        layout.addWidget(self.cutoff_slider)

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        low = self.low_slider.value() / 10.0
        high = self.high_slider.value() / 10.0
        cutoff = self.cutoff_slider.value()
        self.apply_callback(low, high, cutoff)  # callback per applicare il filtro
        self.close()


class MedianFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Mediano")

        layout = QVBoxLayout(self)

        self.ksize_slider = QSlider(Qt.Horizontal)
        self.ksize_slider.setMinimum(1)
        self.ksize_slider.setMaximum(11)
        self.ksize_slider.setValue(3)
        self.ksize_label = QLabel(f"Kernel size: {self.ksize_slider.value()}", self)
        self.ksize_slider.valueChanged.connect(
            lambda: self.ksize_label.setText(f"Kernel size: {self.ksize_slider.value()}"))

        layout.addWidget(self.ksize_label)
        layout.addWidget(self.ksize_slider)

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        ksize = self.ksize_slider.value()
        self.apply_callback(ksize)
        self.close()


class ShockFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Shock")

        layout = QVBoxLayout(self)

        self.iterations_slider = QSlider(Qt.Horizontal)
        self.iterations_slider.setMinimum(1)
        self.iterations_slider.setMaximum(100)
        self.iterations_slider.setValue(10)
        self.iterations_label = QLabel(f"Iterazioni: {self.iterations_slider.value()}", self)
        self.iterations_slider.valueChanged.connect(
            lambda: self.iterations_label.setText(f"Iterazioni: {self.iterations_slider.value()}"))

        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_slider)

        button_layout = QHBoxLayout()

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.apply_callback = apply_callback

    def apply_filter(self):
        iterations = self.iterations_slider.value()
        self.apply_callback(iterations)
        self.close()


class MeanFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Media Aritmetica")

        layout = QVBoxLayout(self)

        self.kernel_size_slider = QSlider(Qt.Horizontal)
        self.kernel_size_slider.setMinimum(3)
        self.kernel_size_slider.setMaximum(15)
        self.kernel_size_slider.setValue(3)
        self.kernel_size_label = QLabel(f"Kernel Size: {self.kernel_size_slider.value()}", self)
        self.kernel_size_slider.valueChanged.connect(
            lambda: self.kernel_size_label.setText(f"Kernel Size: {self.kernel_size_slider.value()}"))

        layout.addWidget(self.kernel_size_label)
        layout.addWidget(self.kernel_size_slider)

        button_layout = QHBoxLayout()

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.apply_callback = apply_callback

    def apply_filter(self):
        kernel_size = self.kernel_size_slider.value()
        self.apply_callback(kernel_size)
        self.close()


class GeometricMeanFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Media Geometrica")

        layout = QVBoxLayout(self)

        self.kernel_size_slider = QSlider(Qt.Horizontal)
        self.kernel_size_slider.setMinimum(3)
        self.kernel_size_slider.setMaximum(15)
        self.kernel_size_slider.setValue(3)
        self.kernel_size_label = QLabel(f"Kernel Size: {self.kernel_size_slider.value()}", self)
        self.kernel_size_slider.valueChanged.connect(
            lambda: self.kernel_size_label.setText(f"Kernel Size: {self.kernel_size_slider.value()}"))

        layout.addWidget(self.kernel_size_label)
        layout.addWidget(self.kernel_size_slider)

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        kernel_size = self.kernel_size_slider.value()
        self.apply_callback(kernel_size)
        self.close()


class LogGeometricMeanFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Media Geometrica Logaritmica")

        layout = QVBoxLayout(self)

        self.kernel_size_slider = QSlider(Qt.Horizontal)
        self.kernel_size_slider.setMinimum(3)
        self.kernel_size_slider.setMaximum(15)
        self.kernel_size_slider.setValue(3)
        self.kernel_size_label = QLabel(f"Kernel Size: {self.kernel_size_slider.value()}", self)
        self.kernel_size_slider.valueChanged.connect(
            lambda: self.kernel_size_label.setText(f"Kernel Size: {self.kernel_size_slider.value()}"))

        layout.addWidget(self.kernel_size_label)
        layout.addWidget(self.kernel_size_slider)

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        kernel_size = self.kernel_size_slider.value()
        self.apply_callback(kernel_size)
        self.close()


class GaussianFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Gaussiano")

        layout = QVBoxLayout(self)

        self.kernel_size_slider = QSlider(Qt.Horizontal)
        self.kernel_size_slider.setMinimum(1)
        self.kernel_size_slider.setMaximum(15)
        self.kernel_size_slider.setValue(5)
        self.kernel_size_label = QLabel(f"Kernel Size: {self.kernel_size_slider.value()}", self)
        self.kernel_size_slider.valueChanged.connect(
            lambda: self.kernel_size_label.setText(f"Kernel Size: {self.kernel_size_slider.value()}")
        )

        layout.addWidget(self.kernel_size_label)
        layout.addWidget(self.kernel_size_slider)

        self.sigma_slider = QSlider(Qt.Horizontal)
        self.sigma_slider.setMinimum(1)
        self.sigma_slider.setMaximum(50)
        self.sigma_slider.setValue(10)
        self.sigma_label = QLabel(f"Sigma: {self.sigma_slider.value() / 10.0}", self)
        self.sigma_slider.valueChanged.connect(
            lambda: self.sigma_label.setText(f"Sigma: {self.sigma_slider.value() / 10.0}")
        )

        layout.addWidget(self.sigma_label)
        layout.addWidget(self.sigma_slider)

        button_layout = QHBoxLayout()
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.apply_callback = apply_callback

    def apply_filter(self):
        kernel_size = self.kernel_size_slider.value()
        sigma = self.sigma_slider.value() / 10.0
        self.apply_callback(kernel_size, sigma)
        self.close()


class ContraHarmonicMeanFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Contra-Harmonic Mean")

        layout = QVBoxLayout(self)

        self.kernel_size_slider = QSlider(Qt.Horizontal)
        self.kernel_size_slider.setMinimum(1)
        self.kernel_size_slider.setMaximum(15)
        self.kernel_size_slider.setValue(3)
        self.kernel_size_label = QLabel(f"Kernel Size: {self.kernel_size_slider.value()}", self)
        self.kernel_size_slider.valueChanged.connect(
            lambda: self.kernel_size_label.setText(f"Kernel Size: {self.kernel_size_slider.value()}")
        )

        layout.addWidget(self.kernel_size_label)
        layout.addWidget(self.kernel_size_slider)

        self.q_slider = QSlider(Qt.Horizontal)
        self.q_slider.setMinimum(-50)
        self.q_slider.setMaximum(50)
        self.q_slider.setValue(10)
        self.q_label = QLabel(f"Q: {self.q_slider.value() / 10.0}", self)
        self.q_slider.valueChanged.connect(
            lambda: self.q_label.setText(f"Q: {self.q_slider.value() / 10.0}")
        )

        layout.addWidget(self.q_label)
        layout.addWidget(self.q_slider)

        button_layout = QHBoxLayout()
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.apply_callback = apply_callback

    def apply_filter(self):
        kernel_size = self.kernel_size_slider.value()
        Q_value = self.q_slider.value() / 10.0
        self.apply_callback(kernel_size, Q_value)
        self.close()


class NotchFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Notch")

        layout = QVBoxLayout(self)

        self.d0_slider = QSlider(Qt.Horizontal)
        self.d0_slider.setMinimum(1)
        self.d0_slider.setMaximum(100)
        self.d0_slider.setValue(30)
        self.d0_label = QLabel(f"d0: {self.d0_slider.value()}", self)
        self.d0_slider.valueChanged.connect(
            lambda: self.d0_label.setText(f"d0: {self.d0_slider.value()}")
        )

        layout.addWidget(self.d0_label)
        layout.addWidget(self.d0_slider)

        self.uk_input = QLineEdit(self)
        self.uk_input.setPlaceholderText("Inserisci u_k (es. 10, -10)")
        layout.addWidget(QLabel("u_k (lista di valori separati da virgola):"))
        layout.addWidget(self.uk_input)

        self.vk_input = QLineEdit(self)
        self.vk_input.setPlaceholderText("Inserisci v_k (es. 0, 0)")
        layout.addWidget(QLabel("v_k (lista di valori separati da virgola):"))
        layout.addWidget(self.vk_input)

        button_layout = QHBoxLayout()
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.apply_callback = apply_callback

    def apply_filter(self):
        try:
            d0 = self.d0_slider.value()

            u_k = list(map(int, self.uk_input.text().split(',')))
            v_k = list(map(int, self.vk_input.text().split(',')))

            if len(u_k) != len(v_k):
                raise ValueError("Le liste di u_k e v_k devono avere la stessa lunghezza.")

            self.apply_callback(d0, u_k, v_k)
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, "Errore", f"Input non valido: {str(e)}")


class AnisotropicDiffusionDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Diffusione Anisotropica")

        layout = QVBoxLayout(self)

        self.iterations_slider = QSlider(Qt.Horizontal)
        self.iterations_slider.setMinimum(1)
        self.iterations_slider.setMaximum(50)
        self.iterations_slider.setValue(10)
        self.iterations_label = QLabel(f"Iterazioni: {self.iterations_slider.value()}", self)
        self.iterations_slider.valueChanged.connect(
            lambda: self.iterations_label.setText(f"Iterazioni: {self.iterations_slider.value()}"))

        self.k_slider = QSlider(Qt.Horizontal)
        self.k_slider.setMinimum(5)
        self.k_slider.setMaximum(100)
        self.k_slider.setValue(15)
        self.k_label = QLabel(f"K: {self.k_slider.value()}", self)
        self.k_slider.valueChanged.connect(lambda: self.k_label.setText(f"K: {self.k_slider.value()}"))

        self.gamma_slider = QSlider(Qt.Horizontal)
        self.gamma_slider.setMinimum(1)
        self.gamma_slider.setMaximum(100)
        self.gamma_slider.setValue(10)
        self.gamma_label = QLabel(f"Gamma: {self.gamma_slider.value() / 100.0}", self)
        self.gamma_slider.valueChanged.connect(
            lambda: self.gamma_label.setText(f"Gamma: {self.gamma_slider.value() / 100.0}"))

        self.option1_radio = QRadioButton("Opzione 1 (esponenziale)")
        self.option2_radio = QRadioButton("Opzione 2 (razionale)")
        self.option1_radio.setChecked(True)

        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_slider)
        layout.addWidget(self.k_label)
        layout.addWidget(self.k_slider)
        layout.addWidget(self.gamma_label)
        layout.addWidget(self.gamma_slider)
        layout.addWidget(self.option1_radio)
        layout.addWidget(self.option2_radio)

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

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


class L1TVDeconvolutionDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Deconvoluzione ℓ1-TV")

        layout = QVBoxLayout(self)

        self.iterations_slider = QSlider(Qt.Horizontal)
        self.iterations_slider.setMinimum(1)
        self.iterations_slider.setMaximum(100)
        self.iterations_slider.setValue(50)
        self.iterations_label = QLabel(f"Iterazioni: {self.iterations_slider.value()}", self)
        self.iterations_slider.valueChanged.connect(
            lambda: self.iterations_label.setText(f"Iterazioni: {self.iterations_slider.value()}"))

        self.reg_weight_slider = QSlider(Qt.Horizontal)
        self.reg_weight_slider.setMinimum(1)
        self.reg_weight_slider.setMaximum(100)
        self.reg_weight_slider.setValue(1)
        self.reg_weight_label = QLabel(f"Peso regolarizzazione: {self.reg_weight_slider.value() / 1000.0}", self)
        self.reg_weight_slider.valueChanged.connect(
            lambda: self.reg_weight_label.setText(f"Peso regolarizzazione: {self.reg_weight_slider.value() / 1000.0}"))

        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_slider)
        layout.addWidget(self.reg_weight_label)
        layout.addWidget(self.reg_weight_slider)

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        iterations = self.iterations_slider.value()
        regularization_weight = self.reg_weight_slider.value() / 1000.0
        self.apply_callback(iterations, regularization_weight)
        self.close()


class WienerFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Wiener")

        layout = QVBoxLayout(self)

        self.kernel_size_slider = QSlider(Qt.Horizontal)
        self.kernel_size_slider.setMinimum(1)
        self.kernel_size_slider.setMaximum(15)
        self.kernel_size_slider.setValue(5)
        self.kernel_size_label = QLabel(f"Kernel Size: {self.kernel_size_slider.value()}", self)
        self.kernel_size_slider.valueChanged.connect(
            lambda: self.kernel_size_label.setText(f"Kernel Size: {self.kernel_size_slider.value()}"))

        layout.addWidget(self.kernel_size_label)
        layout.addWidget(self.kernel_size_slider)

        self.noise_slider = QSlider(Qt.Horizontal)
        self.noise_slider.setMinimum(1)
        self.noise_slider.setMaximum(100)
        self.noise_slider.setValue(10)
        self.noise_label = QLabel(f"Rumore: {self.noise_slider.value() / 100.0}", self)
        self.noise_slider.valueChanged.connect(
            lambda: self.noise_label.setText(f"Rumore: {self.noise_slider.value() / 100.0}"))

        layout.addWidget(self.noise_label)
        layout.addWidget(self.noise_slider)

        button_layout = QHBoxLayout()
        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.apply_callback = apply_callback

    def apply_filter(self):
        kernel_size = self.kernel_size_slider.value()
        noise = self.noise_slider.value() / 100.0
        self.apply_callback(kernel_size, noise)
        self.close()


class CrimminsFilterDialog(QDialog):
    def __init__(self, parent, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Filtro Crimmins Speckle Removal")

        layout = QVBoxLayout(self)

        self.iterations_slider = QSlider(Qt.Horizontal)
        self.iterations_slider.setMinimum(1)
        self.iterations_slider.setMaximum(20)
        self.iterations_slider.setValue(1)
        self.iterations_label = QLabel(f"Iterazioni: {self.iterations_slider.value()}", self)
        self.iterations_slider.valueChanged.connect(
            lambda: self.iterations_label.setText(f"Iterazioni: {self.iterations_slider.value()}")
        )

        layout.addWidget(self.iterations_label)
        layout.addWidget(self.iterations_slider)

        apply_button = QPushButton('Applica', self)
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        cancel_button = QPushButton('Cancella', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.apply_callback = apply_callback

    def apply_filter(self):
        iterations = self.iterations_slider.value()
        self.apply_callback(iterations)
        self.close()
