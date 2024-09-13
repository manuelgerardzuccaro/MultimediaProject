from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

class FilterItemWidget(QWidget):
    def __init__(self, filter_name, param, remove_callback):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(f"{filter_name} (parametro: {param})", self)
        self.layout.addWidget(self.label)

        self.remove_button = QPushButton("X", self)
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.clicked.connect(remove_callback)  # Collegare la funzione per rimuovere il filtro
        self.layout.addWidget(self.remove_button)
