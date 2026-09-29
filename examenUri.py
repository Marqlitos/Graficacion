import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

def conversion(imagen):
    img = imagen.astype(np.float32) / 255.0

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    Y  =  0.299  * R + 0.587  * G + 0.114  * B
    Cb = -0.1687 * R - 0.3313 * G + 0.5    * B + 0.5
    Cr =  0.5    * R - 0.4187 * G - 0.0813 * B + 0.5

    Y  = np.clip(Y * 255, 0, 255)
    Cb = np.clip(Cb * 255, 0, 255)
    Cr = np.clip(Cr * 255, 0, 255)

    ycbcr = np.stack([Y, Cb, Cr], axis=2).astype(np.uint8)
    return ycbcr

def show_all_imagen(original: np.ndarray, ycbcr: np.ndarray) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    axes[0, 0].imshow(original)
    axes[0, 0].set_title("Imagen original (RGB)")

    axes[0, 1].imshow(ycbcr)
    axes[0, 1].set_title("Imagen convertida (YCbCr)")

    axes[1, 0].imshow(ycbcr[:, :, 1], cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title("Canal Cb")

    axes[1, 1].imshow(ycbcr[:, :, 2], cmap="gray", vmin=0, vmax=255)
    axes[1, 1].set_title("Canal Cr")

    for axis in axes.flat:
        axis.axis("off")

    fig.tight_layout()
    plt.show()
    
def rgb_2_hsv_custom(imagen: np.ndarray) -> np.ndarray:
    # Fase 1: Normalización
    img_norm = imagen / 255.0
    
    R = img_norm[:,:,0]
    G = img_norm[:,:,1]
    B = img_norm[:,:,2]
    
    # Fase 2: Matrices max, min y c
    m_max = np.maximum(np.maximum(R, G), B)
    m_min = np.minimum(np.minimum(R, G), B)
    c = m_max - m_min
    
    # Fase 3: Saturación
    S = np.where(m_max == 0, 0.0, c/m_max)
    
    # Fase 4: Hue (Tono)
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

if __name__ == "__main__":
    path = r"abstracto.png"
    
    if os.path.exists(path):
        imagen = cv2.imread(path, 1)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        print("Imagen no encontrada. Creando imagen aleatoria.")
        imagen = np.random.randint(0, 255, (255, 255, 3), dtype=np.uint8)

    imagen_ycbcr = conversion(imagen)
    cv2.imwrite(
        "resultado_ycbcr.png",
        cv2.cvtColor(imagen_ycbcr, cv2.COLOR_RGB2BGR),
    )

    # Mostrar las cuatro imágenes solicitadas.
    show_all_imagen(imagen, imagen_ycbcr)
    
    