import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def rgb_2_grayscale(imagen: np.ndarray) -> np.ndarray:
    
    resultado = imagen[:,:,0]*0.58 + imagen[:,:,1]*0.74 + imagen[:,:,2]*0.24
    return resultado

def rgb_2_hsv_custom(imagen: np.ndarray) -> np.ndarray:
    
    img_norm = imagen / 255.0
    
    R = img_norm[:,:,0]
    G = img_norm[:,:,1]
    B = img_norm[:,:,2]
    
    m_max = np.maximum(np.maximum(R, G), B)
    m_min = np.minimum(np.minimum(R, G), B)
    c = m_max - m_min
    
    
    S = np.where(m_max == 0, 0.0, c/m_max)
    
    
    conditions = [
        c == 0.0,
        np.abs(m_max - R) < 1e-7,
        np.abs(m_max - G) < 1e-7,
        np.abs(m_max - B) < 1e-7
    ]
    
    operations = [
        0.0,
        60 * (((G - B)/c)%6),
        60 * (((B - R)/c)+2),
        60 * (((R - G)/c)+4)
    ]
    
    H = np.select(conditions, operations, default=0.0)
    H = np.where(H < 0, H + 360, H)    
    
    return np.stack((H, S, m_max), axis=-1)


def show_all_images(original, gris, hsv, lab):
    plt.figure(figsize=(14, 10))
    
    # Imagen Original
    plt.subplot(2, 2, 1)
    plt.imshow(original)
    plt.title("Original (RGB)")
    plt.axis("off")
    
    # Escala de Grises
    plt.subplot(2, 2, 2)
    plt.imshow(gris, cmap="gray")
    plt.title("Escala de Grises")
    plt.axis("off")
    
    # HSV (Tono)
    plt.subplot(2, 2, 3)
    plt.imshow(hsv[:,:,0], cmap="hsv") 
    plt.title("HSV (Canal H - Tono)")
    plt.axis("off")
    
    # CIELAB
    plt.subplot(2, 2, 4)
    plt.imshow(lab)
    plt.title("CIELAB")
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    path = r"C:\Users\marco\Documents\images.jpg"
    
    if os.path.exists(path):
        imagen = cv2.imread(path, 1)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        print("Imagen no encontrada. Creando imagen aleatoria.")
        imagen = np.random.randint(0, 255, (255, 255, 3), dtype=np.uint8)
        
    # 1. Grises
    imagen_gris = rgb_2_grayscale(imagen)
    
    # 2. HSV
    imagen_hsv = rgb_2_hsv_custom(imagen)
    
    # 3. CIELAB (usando OpenCV nativo)
    imagen_lab = cv2.cvtColor(imagen, cv2.COLOR_RGB2LAB)
    
    # Mostrar figura
    show_all_images(imagen, imagen_gris, imagen_hsv, imagen_lab)