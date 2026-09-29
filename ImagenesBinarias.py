import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import cv2
import matplotlib.pyplot as plt
import os

# Normalization RGB
def normalization_rgb(imagen: np.ndarray) -> np.ndarray | None:
    if imagen.shape[-1] != 3:
        return None
    return imagen / 255.0

# Normalization function
def normalization(imagen: np.ndarray, scale: float = 1.0) -> np.ndarray | None:
    if imagen.size == 0:
        return None
    return ((imagen - imagen.min()) / (imagen.max() - imagen.min() + 1e-10)) * scale

# RGB to grayscale
def rgb_grayscale(imagen: np.ndarray) -> np.ndarray | None:
    if imagen.shape[-1] != 3:
        return None
    resultado = (
        imagen[:, :, 0] * 0.58 +
        imagen[:, :, 1] * 0.74 +
        imagen[:, :, 2] * 0.24
    )
    return resultado

# Grayscale to bin using a threshold
def gray_2_bin_t(imagen: np.ndarray, t: float = 127.0) -> np.ndarray | None:
    if len(imagen.shape) != 2:
        return None
    return np.where(imagen > t, 1.0, 0.0)

# Grayscale to bin using the median
def gray_2_bin_m(imagen: np.ndarray) -> np.ndarray | None:
    if len(imagen.shape) != 2:
        return None
    median = np.median(imagen)
    return np.where(imagen > median, 1.0, 0.0)

# Otsu method
def otsu_method(gray_image: np.ndarray) -> float | None:
    if len(gray_image.shape) != 2:
        return None
    hist = np.bincount(gray_image.flatten().astype(np.uint8), minlength=256)
    p = hist / gray_image.size
    intensities = np.arange(0, 256, dtype=np.float64)

    w0 = np.cumsum(p)
    w1 = 1 - w0

    mu0 = np.cumsum(intensities * p) / (w0 + 1e-10)
    mu1 = (mu0[-1] - mu0) / (w1 + 1e-10)

    var = w0 * w1 * (mu0 - mu1) ** 2
    return float(np.argmax(var))

# Erosión
def erosion(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) != 2:
        return None
    pad_size = kernel_size // 2
    pad_image = np.pad(bin_image, pad_width=pad_size, mode="constant", constant_values=0)
    window_image = sliding_window_view(pad_image, window_shape=(kernel_size, kernel_size))
    return np.all(window_image == 1.0, axis=(2, 3)).astype(np.float64)

# Dilatación
def dilatation(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) != 2:
        return None
    pad_size = kernel_size // 2
    pad_image = np.pad(bin_image, pad_width=pad_size, mode="constant", constant_values=0)
    window_image = sliding_window_view(pad_image, window_shape=(kernel_size, kernel_size))
    return np.any(window_image == 1.0, axis=(2, 3)).astype(np.float64)

# Apertura
def apertura(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) != 2:
        return None
    img_e = erosion(bin_image, kernel_size)
    img_d = dilatation(img_e, kernel_size)
    return img_d

# Cerradura
def cerradura(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) != 2:
        return None
    img_d = dilatation(bin_image, kernel_size)
    img_e = erosion(img_d, kernel_size)
    return img_e

# Esqueletización
def esqueletizacion(bin_image: np.ndarray) -> np.ndarray | None:
    if len(bin_image.shape) != 2:
        return None
    img = (bin_image * 255).astype(np.uint8)
    skel = np.zeros(img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    temp_img = img.copy()
    
    while True:
        eroded = cv2.erode(temp_img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(temp_img, temp)
        skel = np.bitwise_or(skel, temp)
        temp_img = eroded.copy()
        if cv2.countNonZero(temp_img) == 0:
            break
    return (skel > 0).astype(np.float64)


if __name__ == "__main__":
    path = "Abstracto.png"

    if os.path.exists(path):
        imagen = cv2.imread(path, 1)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        imagen = np.random.randint(0, 255, (255, 255, 3), dtype=np.uint8)

    # 1. Escala de grises
    img_gray_norm = normalization_rgb(imagen)
    img_gray_raw = rgb_grayscale(img_gray_norm)
    img_gray = normalization(img_gray_raw, 255.0).astype(np.uint8)

    # 2. Otsu
    t_otsu = otsu_method(img_gray)
    img_otsu = gray_2_bin_t(img_gray, t_otsu)

    # 3. Umbral Global
    img_threshold = gray_2_bin_t(img_gray, 127.0)

    # 4. Mediana
    img_median = gray_2_bin_m(img_gray)

    # 5. Erosión (aramaten ti Otsu binario kas base)
    e_img = erosion(img_otsu, kernel_size=3)

    # 6. Dilatación
    d_img = dilatation(img_otsu, kernel_size=3)

    # 7. Apertura
    img_ap = apertura(img_otsu, kernel_size=3)

    # 8. Cerradura
    img_c = cerradura(img_otsu, kernel_size=3)

    # 9. Esqueletización
    img_skel = esqueletizacion(img_otsu)

    # Panagabangun ti 3x3 Grid a pagbuklan ti amin a 9 nga imagen
    plt.figure(figsize=(14, 12))
    plt.suptitle("OPERACIONES DE PROCESAMIENTO DE IMÁGENES", fontsize=16, fontweight='bold', color='white', y=0.95)

    operations = [
        (img_gray, "1. Escala de Grises", "gray"),
        (img_otsu, "2. Umbral de Otsu", "gray"),
        (img_threshold, "3. Umbral (T = 127)", "gray"),
        (img_median, "4. Binarización por Mediana", "gray"),
        (e_img, "5. Erosión", "gray"),
        (d_img, "6. Dilatación", "gray"),
        (img_ap, "7. Apertura", "gray"),
        (img_c, "8. Cerradura", "gray"),
        (img_skel, "9. Esqueletización", "gray")
    ]

    for i, (img, title, cmap) in enumerate(operations, 1):
        plt.subplot(3, 3, i)
        plt.imshow(img, cmap=cmap)
        plt.title(title, fontsize=11, fontweight="bold")
        plt.axis("off")

    plt.tight_layout()
    plt.show()