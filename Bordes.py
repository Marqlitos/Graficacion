import numpy as np
import cv2 
import matplotlib.pyplot as plt
import os

def bordes(imagen:np.ndarray) -> np.ndarray | None:
    if len (imagen.shape) != 2:
        return
    
    gx = np.array([
        [1,2,1],
        [0,0,0],
        [-1,-2,-1]
    ])
    
    gy = np.array([
            [1,0,-1],
            [2,0,-2],
            [1,0,-1]
    ])
    
    imagen_gx = cv2.filter2Dp(imagen, gx)
    imagen_gy = cv2.filter2Dp(imagen, gy)
    
    resultado = np.sqrt(imagen_gx**2 + imagen_gy**2)
    resultado = np.clip(resultado, 0 ,255)
    return resultado.astype(np.uint8)

def show_image(imagen:np.ndarray, img_borde: np.ndarray) -> None:
    if len(imagen.shape) != 2 or len(img_borde.shape) != 2 :
        return

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(imagen, cmap="gray")
    plt.axis("off")
    plt.title("Imagen original ", fontweight ="bold")
    plt.subplot(1, 2, 2)
    plt.imshow(resultado, cmap="gray")
    plt.axis("off")
    plt.title("Imagen de bordes")
    plt.show()

if __name__ == "__main__":
    path = "Abstracto.png"
    
    if os.path.exists(path):
        imagen = cv2.imread(path, 0)
    else:
        imagen = np.random.randint(255, (250, 250))
    resultado = bordes(imagen)
    show_image(imagen, resultado)