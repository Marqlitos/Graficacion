# Scirpt grises
import cv2
from matplotlib import pyplot as plt

def gris_promedio(imagen):
    resultado = imagen [:,:,0] + imagen [:,:,1] + imagen [:,:,2]
    return resultado/3

def pesos(imagen):
    resultado = imagen [:,:,0]*0.58 + imagen [:,:,1]*0.74 + imagen [:,:,2]*0.24
    return resultado/2



if __name__ == "__main__":
    path = r"C:\Users\marco\Downloads\images.jpg"
    imagen = cv2.imread(path, 1)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    resultado = gris_promedio(imagen)
    plt.imshow(resultado, cmap='gray')
    plt.show()

