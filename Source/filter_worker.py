import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from filters import median_filter, mean_filter, shock_filter, homomorphic_filter, anisotropic_diffusion, \
    median_blur_filter, geometric_mean_filter, log_geometric_mean_filter, l1_tv_deconvolution


class FilterWorker(QThread):
    filter_applied = pyqtSignal(object)

    def __init__(self, image, filters):
        super().__init__()
        self.image = image
        self.filters = filters
        self._is_running = True  # flag per controllare lo stato del thread

    def run(self):
        temp_image = self.image.copy()
        for filter_name, param in self.filters:
            if filter_name == "Filtro Mediano":
                temp_image = median_filter(temp_image, param)
            elif filter_name == "Filtro MedianBlur":
                temp_image = median_blur_filter(temp_image, param)
            elif filter_name == "Filtro Media Aritmetica":
                temp_image = mean_filter(temp_image, param)
            elif filter_name == "Filtro Media Geometrica":
                temp_image = geometric_mean_filter(temp_image, param)
            elif filter_name == "Filtro Media Geometrica Logaritmica":
                temp_image = log_geometric_mean_filter(temp_image, param)
            elif filter_name == "Filtro Shock":
                temp_image = shock_filter(temp_image, param)
            elif filter_name == "Filtro Homomorphic":
                temp_image = homomorphic_filter(temp_image, low=param['low'], high=param['high'], cutoff=param['cutoff'])
            elif filter_name == "Diffusione Anisotropica":
                temp_image = anisotropic_diffusion(temp_image, iterations=param['iterations'], k=param['k'], gamma=param['gamma'], option=param['option'])
            elif filter_name == "Deconvoluzione ℓ1-TV":
                temp_image = l1_tv_deconvolution(temp_image, iterations=param['iterations'], regularization_weight=param['regularization_weight'])

        if self._is_running:  # check se l'operazione è ancora valida
            self.filter_applied.emit(temp_image)

    def stop(self):
        """Serve per fermare il thread in modo sicuro"""
        self._is_running = False
