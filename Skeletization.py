#Script Squeletization
import numpy as np
import cv2
import matplotlib.pyplot as plt

from tareaUri4 import erosion

def esqueleto(imagen: np.ndarray) -> np.ndarray | None:
    img = (imagen > 0).astype(np.uint8)
    esq = np.zeros_like(img)
    
    kernel = np.array([
        [0,1,0],
        [1,1,1],
        [0,1,0]], dtype=np.uint8)
    
    k = np.sum(kernel)
    
    def erosion(img):
        padded = np.pad(img, 1, mode="constant", constant_values=0)
        s = (padded[1:-1, 1:-1] * kernel[1,1] +
             padded[:-2, 1:-1] * kernel[0,1] +
             padded[2:, 1:-1] * kernel[2,1] +
             padded[1:-1, :-2] * kernel[1,0] +
             padded[1:-1, 2:] * kernel[1,2])
        output = np.zeros_like(img)
        output [s == k] = 1
        return output

    def dilatacion(img):
        padded = np.pad(img, 1, mode="constant", constant_values=0)
        s = (padded[1:-1, 1:-1] * kernel[1,1] +
             padded[:-2, 1:-1] * kernel[0,1] +
             padded[2:, 1:-1] * kernel[2,1] +
             padded[1:-1, :-2] * kernel[1,0] +
             padded[1:-1, 2:] * kernel[1,2])
        output = np.zeros_like(img)
        output [s > 0] = 1
        return output

    for i in range (10):
        erode=erosion(img)
        apertura=dilatacion(erode)
        temp = img - apertura
        result=np.maximum(esq, temp)
        img=erode
        return result
    
    
if __name__ == "__main__":
    img  = cv2.imread("images.jpg", 0)
    result=esqueleto(img)
    
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow (img, cmap = "gray")
    plt.subplot(1, 2, 2)
    plt.imshow(result, cmap="gray")
    plt.show()