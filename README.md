# Digital Image Restoration Project

## Introduction

Digital image restoration is crucial in various fields, including diagnostic medicine, video surveillance, and the preservation of historical archives. Images can be degraded by several types of noise, such as Gaussian, salt-and-pepper, or periodic noise, which reduce their quality and utility. Despite advancements in acquisition and transmission techniques, noise remains a significant challenge that can hinder the analysis and interpretation of images.

This project aims to develop a software system that allows users to improve the visual quality of degraded images through the application of filters and deconvolution techniques. Four images, both in color and grayscale, were selected, and three distinct types of noise were applied. Various filtering algorithms were then used for restoration, with the goal of evaluating the effectiveness of each filter based on the type of noise present.

## Key Objectives

The main goals of this project are:

- Implementing an intuitive user interface to facilitate the application of filters.
- Automating the collection of result data in CSV files for in-depth analysis.
- Evaluating whether the applied filters improve the quality of noisy images compared to the originals using quantitative metrics.

## Features

The software is designed with a modular structure, allowing for easy extension with new filters and functionalities. The graphical user interface (GUI), developed with PyQt5, ensures an intuitive user experience, enabling efficient management of the restoration process.

## Future Directions

The project also considers future developments, including:

- Integration of advanced deep learning techniques, such as Convolutional Neural Networks (CNNs) and Generative Adversarial Networks (GANs).
- Performance optimization through parallel processing on GPUs.

These advancements will make the system more efficient and suitable for more complex applications.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/digital-image-restoration.git
