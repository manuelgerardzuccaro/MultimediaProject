import sys
from PyQt5.QtWidgets import QApplication
from gui import ImageRestorationApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageRestorationApp()
    window.show()
    sys.exit(app.exec_())
