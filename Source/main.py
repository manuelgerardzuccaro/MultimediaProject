from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys
from gui import ImageRestorationApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Imposta un font globale più grande
    app.setFont(QFont("Arial", 14))  # Imposta il font e la dimensione

    window = ImageRestorationApp()
    window.show()
    sys.exit(app.exec_())
