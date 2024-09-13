import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from filters import median_filter, mean_filter


class FilterWorker(QThread):
    filter_applied = pyqtSignal(np.ndarray)

    def __init__(self, image, filters):
        super().__init__()
        self.image = image
        self.filters = filters

    def run(self):
        temp_image = self.image.copy()
        for filter_name, param in self.filters:
            if filter_name == "Filtro Mediano":
                temp_image = median_filter(temp_image, param)
            elif filter_name == "Filtro Media Aritmetica":
                temp_image = mean_filter(temp_image, param)

        self.filter_applied.emit(temp_image)
