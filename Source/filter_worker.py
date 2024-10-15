import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from filters import median_filter, mean_filter, shock_filter, homomorphic_filter, anisotropic_diffusion, \
    median_blur_filter, geometric_mean_filter, log_geometric_mean_filter, l1_tv_deconvolution, wiener_deconvolution, \
    add_gaussian_noise, add_salt_pepper_noise, add_uniform_noise, add_film_grain_noise, add_periodic_noise, \
    gaussian_filter, contra_harmonic_mean_filter, notch_filter, crimmins_speckle_removal


class FilterWorker(QThread):
    filter_applied = pyqtSignal(object)

    def __init__(self, image, filters):
        super().__init__()
        self.image = image
        self.filters = filters
        self._is_running = True  # flag per controllare lo stato del thread

    def run(self):
        temp_image = self.image.copy()

        filter_functions = {
            "Filtro Mediano": lambda img, param: median_filter(img, param),
            "Filtro MedianBlur": lambda img, param: median_blur_filter(img, param),
            "Filtro Media Aritmetica": lambda img, param: mean_filter(img, param),
            "Filtro Media Geometrica": lambda img, param: geometric_mean_filter(img, param),
            "Filtro Media Geometrica Logaritmica": lambda img, param: log_geometric_mean_filter(img, param),
            "Filtro Gaussiano": lambda img, param: gaussian_filter(img, kernel_size=param['kernel_size'],
                                                                   sigma=param['sigma']),
            "Filtro Contra-Harmonic Mean": lambda img, param: contra_harmonic_mean_filter(img, kernel_size=param[
                'kernel_size'], Q=param['Q']),
            "Filtro Notch": lambda img, param: notch_filter(img, d0=param['d0'], u_k=param['u_k'], v_k=param['v_k']),
            "Filtro Shock": lambda img, param: shock_filter(img, param),
            "Filtro Homomorphic": lambda img, param: homomorphic_filter(img, low=param['low'], high=param['high'],
                                                                        cutoff=param['cutoff']),
            "Diffusione Anisotropica": lambda img, param: anisotropic_diffusion(img, iterations=param['iterations'],
                                                                                k=param['k'], gamma=param['gamma'],
                                                                                option=param['option']),
            "Deconvoluzione ℓ1-TV": lambda img, param: l1_tv_deconvolution(img, iterations=param['iterations'],
                                                                           regularization_weight=param[
                                                                               'regularization_weight']),
            "Deconvoluzione Wiener": lambda img, param: wiener_deconvolution(img, param['kernel_size'], param['noise']),
            "Filtro Crimmins Speckle Removal": lambda img, param: crimmins_speckle_removal(img, iterations=param),
            "Rumore Gaussiano": lambda img, _: add_gaussian_noise(img),
            "Rumore Sale e Pepe": lambda img, _: add_salt_pepper_noise(img),
            "Rumore Uniforme": lambda img, _: add_uniform_noise(img),
            "Rumore Grana della Pellicola": lambda img, _: add_film_grain_noise(img),
            "Rumore Periodico": lambda img, _: add_periodic_noise(img),
        }

        for filter_name, param in self.filters:
            if not self._is_running:
                break  # Esce dal loop se l'operazione non è più valida

            filter_func = filter_functions.get(filter_name)
            if filter_func:
                try:
                    temp_image = filter_func(temp_image, param)
                except Exception as e:
                    print(f"Errore durante l'applicazione del filtro '{filter_name}': {e}")
                    continue  # Continua con il filtro successivo
            else:
                print(f"Filtro non riconosciuto: '{filter_name}'")
                continue

        if self._is_running:
            self.filter_applied.emit(temp_image)

    def stop(self):
        """Serve per fermare il thread in modo sicuro"""
        self._is_running = False
