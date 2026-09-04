#Script para calcular imagenes binarias
import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

#Normalization function
def normalization (imagen:np.ndarray, scale:float = 1.0) -> np.ndarray | None:
    if len (imagen) == 0:
        return
    
    return ((imagen - imagen.min())/(imagen.max() - imagen.min())) * scale

#RGB to grayscale
def rgb_2_grayscale(imagen:np.ndarray) -> np.ndarray | None:
    if imagen.shape[-1] > 3 or imagen.shape[-1] < 3:
        return
    
    resultado = imagen[:,:,0]*0.58 + imagen[:,:,1]*0.74 + imagen[:,:,2]*0.24
     
    return resultado

#Grayscale to bin using a threshold
def gray_2_bin_t(imagen:np.ndarray, t:float=127.0) -> np.ndarray | None:
    if len(imagen.shape) > 2 or len (imagen.shape) < 2:
        return
    
    return np.where(imagen > t, 1.0,0.0)

#Grayscale to bin using the median
def gray_2_bin_m(imagen:np.ndarray) -> np.ndarray | None:
    if len (imagen.shape) > 2 or len (imagen.shape) < 2:
        return
    
    median = np.median (imagen.reshape (-1))
    return np.where (imagen > median, 1.0, 0.0)

#Show image function
def show_image(image:np.ndarray, bin_image:np.ndarray) -> None:
    plt.figure (figsize=(12,8))
    plt.subplot (1,2,1)
    plt.imshow (image, cmap= "gray")
    plt.axis ("off")
    plt.title("Original image")
    plt.subplot(1, 2, 2)
    plt.imshow(bin_image.astype(np.uint8), cmap= "gray")
    plt.axis("off")
    plt.title("Binary image")
    plt.show()
        
if __name__ == "__main__":
    path = r"C:\Users\marco\Documents\images.jpg"
        
    if os.path.exists(path):
        imagen = cv2.imread(path,1)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        imagen = np.random.randint (0,255, (255,255,3), dtype=np.uint8)

    gray_image = rgb_2_grayscale (imagen)
        
    #umbral image
    bin_image_t = gray_2_bin_t (gray_image)
        
    #Mean bin image
    bin_image_m = gray_2_bin_m (gray_image)
        
    #show image
    show_image(gray_image, bin_image_t)
    show_image(gray_image, bin_image_m)
    
    