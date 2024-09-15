import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from filters import median_filter, mean_filter, shock_filter, homomorphic_filter


class FilterWorker(QThread):
    filter_applied = pyqtSignal(object)

    def __init__(self, image, filters):
        super().__init__()
        self.image = image
        self.filters = filters
        self._is_running = True  # Flag per controllare lo stato del thread

    def run(self):
        temp_image = self.image.copy()
        for filter_name, param in self.filters:
            if filter_name == "Filtro Mediano":
                temp_image = median_filter(temp_image, param)
            elif filter_name == "Filtro Media Aritmetica":
                temp_image = mean_filter(temp_image, param)
            elif filter_name == "Filtro Shock":
                temp_image = shock_filter(temp_image, param)
            elif filter_name == "Filtro Homomorphic":
                temp_image = homomorphic_filter(temp_image, low=param['low'], high=param['high'], cutoff=param['cutoff'])

        if self._is_running:  # Verifica se l'operazione è ancora valida
            self.filter_applied.emit(temp_image)

    def stop(self):
        """Metodo per fermare il thread in modo sicuro"""
        self._is_running = False
