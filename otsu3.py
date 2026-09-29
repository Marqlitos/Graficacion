import numpy as np
import cv2
import os
from numpy.lib.stride_tricks import sliding_window_view
import matplotlib.pyplot as plt


# Normalization RGB
def normalization_rgb(imagen: np.ndarray) -> np.ndarray | None:
    if len(imagen.shape) != 3 or imagen.shape[-1] != 3:
        return

    return imagen / 255.0


# RGB to grayscale
def rgb_2_grayscale(imagen: np.ndarray) -> np.ndarray | None:
    if len(imagen.shape) != 3 or imagen.shape[-1] != 3:
        return

    resultado = (
        imagen[:, :, 0] * 0.58 +
        imagen[:, :, 1] * 0.74 +
        imagen[:, :, 2] * 0.24
    )

    return resultado


# Normalization function
def normalization(imagen: np.ndarray, scale: float = 1.0) -> np.ndarray | None:
    if len(imagen.shape) < 2 or len(imagen.shape) > 2:
        return

    if imagen.max() == imagen.min():
        return np.zeros_like(imagen)

    return ((imagen - imagen.min()) /
            (imagen.max() - imagen.min())) * scale


# Grayscale to binary using a threshold
def gray_2_bin_t(
    imagen: np.ndarray,
    t: float = 127.0
) -> np.ndarray | None:

    if len(imagen.shape) != 2:
        return

    return np.where(imagen > t, 1.0, 0.0)


# Grayscale to binary using the median
def gray_2_bin_m(imagen: np.ndarray) -> np.ndarray | None:

    if len(imagen.shape) != 2:
        return

    median = np.median(imagen.reshape(-1))

    return np.where(imagen > median, 1.0, 0.0)


# Show image function
def show_image(image: np.ndarray, bin_image: np.ndarray) -> None:

    plt.figure(figsize=(12, 8))

    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    plt.title("Original image")

    plt.subplot(1, 2, 2)
    plt.imshow(bin_image.astype(np.uint8), cmap="gray")
    plt.axis("off")
    plt.title("Binary image")

    plt.show()


# Otsu method
def otsu_method(gray_image: np.ndarray) -> np.ndarray | None:

    if len(gray_image.shape) != 2:
        return

    # Step 1: Histogram
    hist = np.bincount(
        gray_image.flatten().astype(np.uint8),
        minlength=256
    )

    p = hist / gray_image.size

    intensities = np.arange(0,256,dtype=np.float64)

    # Step 2: Probabilities
    w0 = np.cumsum(p)
    w1 = 1 - w0

    # Step 3: Mean
    mu0 = np.cumsum(intensities * p) / (w0 + 1e-10)

    mu1 = (
        mu0[-1] - np.cumsum(intensities * p)
    ) / (w1 + 1e-10)

    # Step 4: Between-class variance
    var = w0 * w1 * (mu0 - mu1) ** 2

    return np.argmax(var)


# Erosion method
def erosion(bin_image: np.ndarray,kernel_size: int = 3) -> np.ndarray | None:

    if len(bin_image.shape) != 2:
        return

    pad_size = kernel_size // 2

    # Padding image
    pad_image = np.pad(bin_image, pad_width=pad_size, mode="constant", constant_values=255)

    # Window sliding kernel
    window_image = sliding_window_view(pad_image,window_shape=(kernel_size, kernel_size))

    return np.all(window_image == 255, axis=(2, 3)).astype(np.uint8) * 255


# Dilation method
def dilatation(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) != 2:
        return
    pad_size = kernel_size // 2

    # Padding image
    pad_image = np.pad(bin_image,pad_width=pad_size, mode="constant", constant_values=255)

    # Window
    window_image = sliding_window_view(pad_image,window_shape=(kernel_size, kernel_size))
    return np.any(window_image == 255, axis=(2, 3)).astype(np.uint8) * 255

#cerradura
def cerradura (bin_image:np.ndarray) -> np.ndarray | None:
    if len(bin_image.shape) > 2 or len (bin_image.shape) <2:
        return
    img_dil = dilatation(bin_image)
    img_e = erosion(img_dil)

#apertura
def cerradura (bin_image:np.ndarray) -> np.ndarray | None:
    if len(bin_image.shape) > 2 or len (bin_image.shape) <2:
        return
    img_dil = dilatation(bin_image)
    img_e = erosion(img_dil)

if __name__ == "__main__":
    path = "Abstracto.png"
    if os.path.exists(path):

        imagen = cv2.imread(path, 1)
        imagen = cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)
    else:
        imagen = np.random.randint(0,255, (255, 255, 3),dtype=np.uint8)

    # Normalization RGB
    img_rgb = normalization_rgb(imagen)
    # RGB to grayscale
    img_gray = rgb_2_grayscale(img_rgb)
    # Normalization grayscale
    img_gray = normalization(img_gray, 255.0).astype(np.uint8)
    # Otsu method
    t = otsu_method(img_gray)
    print("Threshold Otsu:", t)
    img_otsu = gray_2_bin_t(img_gray,t)
    # Erosion
    e_img = erosion(img_otsu * 255.0, 12)
    # Dilation
    d_img = dilatation(img_otsu * 255.0, 12)
    # Show images
    show_image(img_otsu * 255.0, e_img)
    show_image(img_otsu * 255.0,d_img)
    
    