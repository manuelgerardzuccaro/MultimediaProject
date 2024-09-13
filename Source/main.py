from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys
from gui import ImageRestorationApp
import os


def create_directories():
    """Crea le cartelle 'SavedImages' e 'FilterConfig' se non esistono."""
    directories = ["SavedImages", "FilterConfig"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Cartella '{directory}' creata.")
        else:
            print(f"Cartella '{directory}' già esistente.")



if __name__ == "__main__":
    create_directories()

    app = QApplication(sys.argv)

    # Imposta un font globale più grande
    app.setFont(QFont("Arial", 14))  # Imposta il font e la dimensione

    window = ImageRestorationApp()
    window.show()
    sys.exit(app.exec_())
