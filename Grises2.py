#clase para escala de grises

import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

class escala_grises:

    def __init__(self, imagen:np.ndarray):
        self.imagen = imagen

    def procesamiento (self, tipo : str):
        if tipo == "promedio": 
            return self.promedio()

    def  promedio (self) -> np.ndarray:
        resultado = self.imagen [:,:,0] + self.imagen [:,:,1] + self.imagen [:,:,2]
        return resultado / 3

    def _luminosidad (self) -> np.ndarray:
        resultado = self.imagen [:,:,0] + 0.78 * self.imagen [:,:,1] + 0.24 *self.imagen [:,:,2] + 0.74
        return resultado /3

if __name__ == "__main__":
    path = "C:\\Users\\marco\\Downloads\\60234ca9-14eb-4809-9def-e527c6633e5c.png"

    if os.path.exists(path):
        imagen = cv2.imread (path, 1)
        imagen = cv2.cvtColor (imagen, cv2.COLOR_BGR2RGB)
    else:
        print ("Path no encontrada, creando imagen sintetica")
        imagen = np.random.randint (0, 255, (250, 250,3), dtype= np.uint8)

    es = escala_grises (imagen)
    resultado = es.procesamiento ("promedio")
    plt.imshow(resultado)
    plt.show()
