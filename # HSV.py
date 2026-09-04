# HSV
# Hue Saturation Value
# Tono Saturacion Valor

import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

#Normalization Method
def normalization (imagen:np.ndarray) -> np.ndarray:
    return imagen / 255.0

#Max, Min, and c matrices
def matrices (imagen:np.ndarray) -> np.ndarray | None:
    if np.max (imagen) > 1.0 or np.min (imagen) < 0:
        print ("Imagen no normalizada...")
        return
    
    R = imagen [:,:,0]
    G = imagen [:,:,1]
    B = imagen [:,:,2]
    
    m_max = np.maximum (np.maximum (R, G), B)
    m_min = np.minimum (np.minimum (R, G), B)
    c = m_max - m_min
    
    return m_max, m_min, c 

#Saturation function
def saturation (m_max:np.ndarray, c:np.ndarray) -> np.ndarray:
    return np.where(m_max == 0, 0.0, c/m_max)

#Hue Function
def hue (img_norm:np.ndarray, m_max:np.ndarray, c:np.ndarray) -> np.ndarray:
    
    R = img_norm[:,:,0]
    G = img_norm[:,:,1]
    B = img_norm[:,:,2]
    
    conditions = [
        c == 0.0,
        np.abs(m_max - R)<1e-7,
        np.abs(m_max - G)<1e-7,
        np.abs(m_max - B)<1e-7
    ]
    
    operations = [
        0.0,
        60 * (((G - B)/c)%6),
        60 * (((B - R)/c)+2),
        60 * (((R - G)/c)+4)
    ]
    
    H = np.select (conditions, operations, default= 0.0) 
    return np.where(H < 0, H + 360, H)    
    
#General function
def rgb_2_hsv_custom(imagen: np.ndarray) -> np.ndarray | None:
    if imagen.shape [-1] < 3 or imagen.shape [-1] > 3:
        print ("Error... formato no valido")
        return
    
    #Phase 1: Normalization
    img_norm = normalization (imagen)
    
    #Phase 2: max, min, and c matrices
    m_max, m_min, c = matrices (img_norm)
    
    #Phase 3:Saturation Function
    S = saturation (m_max, c)
    
    #Phase 4: Hue Function
    H = hue(img_norm, m_max, c)
    return np.stack ((H, S, m_max), axis= -1)
    
#Show image
def show_image(hsv_image:np.ndarray) -> None:
    if hsv_image.shape [-1] > 3 or hsv_image.shape[-1] <3:
        return
    
    plt.figure(figsize=(12,8))
    plt.subplot(2, 2, 1)
    plt.imshow(hsv_image, cmap="hsv")
    plt.axis("off")
    plt.subplot(2, 2, 2)
    plt.imshow(hsv_image[:,:,0], cmap="hsv")
    plt.axis("off")
    plt.subplot(2, 2, 3)
    plt.imshow(hsv_image[:,:,1], cmap="magma")
    plt.axis("off")
    plt.subplot(2, 2, 4)
    plt.imshow(hsv_image[:,:,2], cmap="Blues")
    plt.axis("off")
    plt.show()
    
if __name__ == "__main__":
    path = ""
    
    if os.path.exists(path):
        imagen = cv2.imread(path,1)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        imagen = np.random.randint (0,255, (255,255, 3), dtype=np.uint8)
    
    resultado = rgb_2_hsv_custom(imagen)
    show_image(resultado)    