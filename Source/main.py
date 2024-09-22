from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys
from gui import ImageRestorationApp
import os


def create_directories():
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
    app.setFont(QFont("Arial", 14), None)  # Imposta il font e la dimensione

    window = ImageRestorationApp()
    window.show()

    sys.exit(app.exec_())
