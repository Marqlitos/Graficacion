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

imagen = cv2.imread("Abstracto.png", 1)
print(imagen.shape)
imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

resultado = conversion(imagen)

cv2.imwrite('resultado_ycbcr.jpg', cv2.cvtColor(resultado, cv2.COLOR_RGB2BGR))
#plt.imshow(resultado)
#plt.show
conversion(resultado)