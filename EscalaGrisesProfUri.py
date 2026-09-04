# Script grises
import cv2
import numpy as np 
from matplotlib import pyplot as plt

def gris_promedio(imagen):
    img_float = imagen.astype(float) 
    resultado = (img_float[:,:,0] + img_float[:,:,1] + img_float[:,:,2]) / 3
    return resultado

def pesos(imagen):
    img_float = imagen.astype(float)
    resultado = img_float[:,:,0]*0.58 + img_float[:,:,1]*0.74 + img_float[:,:,2]*0.24
    return resultado

def luminosidad(imagen):
    img_float = imagen.astype(float)
    maximo = np.max(img_float, axis=2)
    minimo = np.min(img_float, axis=2)
    resultado = (maximo + minimo) / 2
    return resultado


if __name__ == "__main__":
    path = r"C:\Users\marco\Downloads\images.jpg"
    imagen = cv2.imread(path, 1)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    resultado = pesos(imagen)
    #resultado = gris_promedio(imagen) 
    #resultado = luminosidad(imagen) 
    
    plt.imshow(resultado, cmap='gray')
    plt.show()