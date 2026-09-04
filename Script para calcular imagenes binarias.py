#Script para calcular imagenes binarias

import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

#Binary image
def gray_2_bin(image:np.ndarray, t:float=128.0):
    if len(image) == 0:
        return
    
    return np.where(image > t, 1.0, 0.0)

#Show image
def show_image(hsv_image:np.ndarray, bin_image:np.ndarray) -> None:
    
    plt.figure(figsize=(12,8))
    plt.subplot(1, 2, 1)
    plt.imshow(imagen)
    plt.axis ("off")
    plt.title("Original image")
    plt.subplot(1, 2, 2)
    plt.imshow(bin_image.astype(np.uint8))
    plt.axis("off")
    plt.title("Binary image")
    plt.show()
    
if __name__ == "__main__":
    path = r"C:\Users\marco\OneDrive\Documents\Graficacion\images.jpg"
    
    if os.path.exists(path):
        imagen = cv2.imread(path,1)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        imagen = np.random.randint (0,255, (255,255), dtype=np.uint8)
        
    R = imagen [:,:,0]
    G = imagen [:,:,1]
    B = imagen [:,:,2]

    R_bin = gray_2_bin(R)
    G_bin = gray_2_bin(G)
    B_bin = gray_2_bin(B)

    resultado = np.stack((R_bin, G_bin, B_bin), axis= -1)
    show_image(imagen,resultado)
    