import os
import cv2
import numpy as np
import pydicom


class ProcesadorDICOM:

    def __init__(self, carpeta):

        self.carpeta = carpeta

        self.archivos = sorted([
            archivo
            for archivo in os.listdir(carpeta)
            if archivo.lower().endswith(".dcm")
        ])

    def numero_cortes(self):
        return len(self.archivos)

    def leer_corte(self, indice):

        ruta = os.path.join(
            self.carpeta,
            self.archivos[indice]
        )

        dicom = pydicom.dcmread(ruta)

        imagen = dicom.pixel_array

        imagen = cv2.normalize(
            imagen,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        imagen = imagen.astype(np.uint8)

        return imagen

    def ecualizar(self, imagen):

        return cv2.equalizeHist(imagen)
    
    def media(self, imagen):

        return cv2.blur(
            imagen,
            (5,5)
        )

    def gaussiano(self, imagen):

        return cv2.GaussianBlur(
            imagen,
            (5,5),
            0
        )

    def sobel(self, imagen):

        sobelx = cv2.Sobel(
            imagen,
            cv2.CV_64F,
            1,
            0,
            ksize=3
        )

        sobely = cv2.Sobel(
            imagen,
            cv2.CV_64F,
            0,
            1,
            ksize=3
        )

        magnitud = cv2.magnitude(
            sobelx,
            sobely
        )

        return cv2.convertScaleAbs(magnitud)

    def laplaciano(self, imagen):

        lap = cv2.Laplacian(
            imagen,
            cv2.CV_64F,
            ksize=3
        )
        lap = cv2.convertScaleAbs(lap)

        return lap

    def binaria(self, imagen, umbral):

        imagen = cv2.GaussianBlur(
            imagen,
            (5,5),
            0
        )

        _, binaria = cv2.threshold(
            imagen,
            umbral,
            255,
            cv2.THRESH_BINARY
        )

        return binaria
    
    def resta(self, imagen):

        gauss = cv2.GaussianBlur(
            imagen,
            (5,5),
            0
        )

        resta = cv2.subtract(
            imagen,
            gauss
        )

        return resta
    
    def fourier(self, imagen):

        f = np.fft.fft2(imagen)

        fshift = np.fft.fftshift(f)

        magnitud = np.log(np.abs(fshift) + 1)

        magnitud = cv2.normalize(
            magnitud,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        return magnitud.astype(np.uint8)
    
    def and_logico(self, imagen, umbral):

        _, mascara = cv2.threshold(
            imagen,
            umbral,
            255,
            cv2.THRESH_BINARY
        )

        resultado = cv2.bitwise_and(
            imagen,
            imagen,
            mask=mascara
        )

        return resultado
    
    def or_logico(self, imagen, umbral):

        _, mascara = cv2.threshold(
            imagen,
            umbral,
            255,
            cv2.THRESH_BINARY
        )

        resultado = cv2.bitwise_or(
            imagen,
            imagen,
            mask=mascara
        )

        return resultado
    
    def histograma(self, imagen, color):

        import matplotlib.pyplot as plt
        from io import BytesIO
        from PIL import Image

        hist = cv2.calcHist(
            [imagen],
            [0],
            None,
            [256],
            [0,256]
        )

        # Crear figura
        fig = plt.figure(
            figsize=(5,3.5),
            facecolor="#2B2B2B"
        )

        ax = fig.add_subplot(111)

        ax.set_facecolor("#2B2B2B")

        # Dibujar histograma con el color recibido
        ax.plot(
            hist,
            color=color,
            linewidth=2
        )

        ax.set_xlabel(
            "Intensidad",
            color="white"
        )

        ax.set_ylabel(
            "Número de píxeles",
            color="white"
        )

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

        ax.grid(alpha=0.10)

        fig.subplots_adjust(
            left=0.18,
            right=0.98,
            bottom=0.20,
            top=0.95
        )

        buffer = BytesIO()

        plt.savefig(
            buffer,
            format="png",
            facecolor=fig.get_facecolor()
        )

        plt.close(fig)

        buffer.seek(0)

        return Image.open(buffer)