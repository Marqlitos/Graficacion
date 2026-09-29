import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import cv2
import matplotlib.pyplot as plt
import os


# Normalization RGB
def normalization_rgb(imagen: np.ndarray) -> np.ndarray | None:
    if imagen.shape[-1] < 3 or imagen.shape[-1] > 3:
        return

    return imagen / 255.0


# Normalization function
def normalization(imagen: np.ndarray, scale: float = 1.0) -> np.ndarray | None:
    if len(imagen) == 0:
        return

    return ((imagen - imagen.min()) /
            (imagen.max() - imagen.min())) * scale


# RGB to grayscale
def rgb_grayscale(imagen: np.ndarray) -> np.ndarray | None:
    if imagen.shape[-1] > 3 or imagen.shape[-1] < 3:
        return

    resultado = (
        imagen[:, :, 0] * 0.58 +
        imagen[:, :, 1] * 0.74 +
        imagen[:, :, 2] * 0.24
    )

    return resultado


# Grayscale to bin using a threshold
def gray_2_bin_t(imagen: np.ndarray, t: float = 127.0) -> np.ndarray | None:
    if len(imagen.shape) > 2 or len(imagen.shape) < 2:
        return

    return np.where(imagen > t, 1.0, 0.0)


# Grayscale to bin using the median
def gray_2_bin_m(imagen: np.ndarray, t: float = 127.0) -> np.ndarray | None:
    if len(imagen.shape) > 2 or len(imagen.shape) < 2:
        return

    median = np.median(imagen.reshape(-1))

    return np.where(imagen > median, 1.0, 0.0)


# Otsu method
def otsu_method(gray_image: np.ndarray) -> np.ndarray | None:
    if len(gray_image.shape) > 2 or len(gray_image.shape) < 2:
        return

    # Step 1: histogram calculation
    hist = np.bincount(
        gray_image.flatten().astype(np.uint8),
        minlength=256
    )

    p = hist / gray_image.size
    intensities = np.arange(0, 256, dtype=np.uint16)

    # Step 2: Weight calculation
    w0 = np.cumsum(p)
    w1 = 1 - w0

    # Step 3: means calculation
    mu0 = np.cumsum(intensities * p) / (w0 + 1e-10)
    mu1 = (mu0[-1] - mu0) / (w1 + 1e-10)

    # Step 4: Variance calculation
    var = w0 * w1 * (mu0 - mu1) ** 2

    return np.argmax(var)


def erosion(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) > 2 or len(bin_image.shape) < 2:
        return

    pad_size = kernel_size // 2

    pad_image = np.pad(
        bin_image,
        pad_width=pad_size,
        mode="constant",
        constant_values=255
    )

    window_image = sliding_window_view(
        pad_image,
        window_shape=(kernel_size, kernel_size)
    )

    return np.any(
        window_image == 255,
        axis=(2, 3)
    ).astype(np.uint8) * 255


def dilatation(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) != 2:
        return

    pad_size = kernel_size // 2

    pad_image = np.pad(
        bin_image,
        pad_width=pad_size,
        mode="constant",
        constant_values=255
    )

    window_image = sliding_window_view(
        pad_image,
        window_shape=(kernel_size, kernel_size)
    )

    return np.all(
        window_image == 255,
        axis=(2, 3)
    ).astype(np.uint8) * 255


# Apertura
def apertura(bin_image: np.ndarray, kernel_size: int = 3) -> np.ndarray | None:
    if len(bin_image.shape) > 2 or len(bin_image.shape) < 2:
        return

    pad_size = kernel_size // 2

    pad_image = np.pad(
        bin_image,
        pad_width=pad_size,
        mode="constant",
        constant_values=255
    )

    window_image = sliding_window_view(
        pad_image,
        window_shape=(kernel_size, kernel_size)
    )

    return (
        np.any(
            window_image == 255,
            axis=(2, 3)
        ).astype(np.uint8) * 255
        +
        np.all(
            window_image == 255,
            axis=(2, 3)
        ).astype(np.uint8) * 255
    )


# Cerradura
def cerradura(bin_image: np.ndarray) -> np.ndarray | None:
    if len(bin_image.shape) > 2 or len(bin_image.shape) < 2:
        return

    img_dil = dilatation(bin_image)
    img_e = erosion(img_dil)

    return img_e


# Aperture
def aperutra(bin_image: np.ndarray) -> np.ndarray | None:
    if len(bin_image.shape) > 2 or len(bin_image.shape) < 2:
        return

    img_dil = erosion(bin_image)
    img_e = dilatation(img_dil)

    return img_e


# Binary image
# Función tomada del segundo código
def gray_2_bin(image: np.ndarray, t: float = 128.0):
    if len(image) == 0:
        return

    return np.where(image > t, 1.0, 0.0)


if __name__ == "__main__":

    path = "auto2.png"

    if os.path.exists(path):
        imagen = cv2.imread(path, 1)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        imagen = np.random.randint(
            0,
            255,
            (255, 255, 3),
            dtype=np.uint8
        )


    # BINARIZACIÓN DE LOS CANALES RGB

    R = imagen[:, :, 0]
    G = imagen[:, :, 1]
    B = imagen[:, :, 2]

    R_bin = gray_2_bin(R)
    G_bin = gray_2_bin(G)
    B_bin = gray_2_bin(B)

    resultado = np.stack(
        (R_bin, G_bin, B_bin),
        axis=-1
    )


    # ESCALA DE GRISES


    img_gray = normalization_rgb(imagen)

    img_gray = rgb_grayscale(img_gray)

    img_gray = normalization(
        img_gray,
        255.0
    ).astype(np.uint8)


    # BINARIZACIÓN POR UMBRAL
    img_threshold = gray_2_bin_t(
        img_gray,
        127
    )


    # BINARIZACIÓN POR MEDIANA

    img_median = gray_2_bin_m(
        img_gray
    )


    # MÉTODO DE OTSU

    t = otsu_method(img_gray)

    img_otsu = gray_2_bin_t(
        img_gray,
        t
    )

    e_img = erosion(
        img_otsu * 255.0
    )


    d_img = dilatation(
        img_otsu * 255.0
    )


    img_ap = apertura(
        img_otsu * 255
    )


    img_c = cerradura(
        img_otsu * 255
    )


    plt.figure(figsize=(15, 10))


    plt.subplot(3, 3, 1)
    plt.imshow(imagen)
    plt.title("Imagen original")
    plt.axis("off")


    plt.subplot(3, 3, 2)
    plt.imshow(resultado * 255.0)
    plt.title("Binario RGB")
    plt.axis("off")


    plt.subplot(3, 3, 3)
    plt.imshow(img_gray, cmap="gray")
    plt.title("Escala de grises")
    plt.axis("off")


    plt.subplot(3, 3, 4)
    plt.imshow(img_threshold, cmap="gray")
    plt.title("Umbral T = 127")
    plt.axis("off")


    plt.subplot(3, 3, 5)
    plt.imshow(img_median, cmap="gray")
    plt.title("Mediana")
    plt.axis("off")


    plt.subplot(3, 3, 6)
    plt.imshow(img_otsu, cmap="gray")
    plt.title("Otsu")
    plt.axis("off")


    plt.subplot(3, 3, 7)
    plt.imshow(e_img, cmap="gray")
    plt.title("Erosion")
    plt.axis("off")


    plt.subplot(3, 3, 8)
    plt.imshow(d_img, cmap="gray")
    plt.title("Dilatation")
    plt.axis("off")


    plt.subplot(3, 3, 9)
    plt.imshow(img_ap, cmap="gray")
    plt.title("Apertura")
    plt.axis("off")


    plt.tight_layout()
    plt.show()


    # Segunda figura para cerradura
    plt.figure(figsize=(6, 5))

    plt.imshow(img_c, cmap="gray")
    plt.title("Cerradura")
    plt.axis("off")

    plt.show()