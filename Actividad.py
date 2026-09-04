import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

#Normalizacion
def normalizacion(imagen:np.ndarray) -> np.ndarray | None:

    if imagen.shape[-1] < 3:
        print("Imagen en espacio de color incorrecto")
        return

    return imagen / 255.0

# X, Y , Z Espacio
def xzy_space(imagen:np.ndarray) -> np.ndarray | None:
    if np.max(imagen) > 1.0:
        print("Aplicar proceso de normalizacion")
        return

    pesos = np.array ([
        [0.4124, 0.3576, 0.1805],
        [0.2126, 0.7152, 0.0722],
        [0.0193, 0.1192, 0.9505],
    ])

    return np.matmul (imagen, pesos.T)

#funcio de Parametrizacion
def f_t (imagen:np.ndarray) -> np.ndarray | None:
    if imagen.shape [-1] < 3:
        print ("Dimensiones incorrectas")
        return

    return np.where(imagen > 0.008856, np.cbrt(imagen),
    7.786 * imagen + (16/116))

#Cielab Space
def cielab_space (imagen:np.ndarray) -> np.ndarray | None:
    if imagen.shape [-1] < 3:
        print ("Dimensiones incorrectas")
        return

    Xn, Yn, Zn = 0.9547, 1.0, 1.108883
    L = 116 * (f_t(imagen[:,:,1]/ Yn)) - 16
    a = 500 * (f_t(imagen[:,:,0]/Xn) - f_t(imagen[:,:,1]/Yn))
    b = 200 * (f_t(imagen[:,:,1]/Xn) - f_t(imagen[:,:,2]/Zn))

    return np.stack ((L, a, b), axis = -1)

#Funcion final
def rgb_2_cielab_custom(imagen:np.ndarray) -> np.ndarray | None:
    if imagen.shape [-1] < 3 or imagen.shape [-1] > 3:
        print("Imagen que no es a color")
        return

    #Step 1: normalization
    img_norm = normalizacion (imagen)

    #Step  2:
    xyz_image = xzy_space (img_norm)

    #step 3: L, a, b Space
    lab_img = cielab_space(xyz_image)
    return lab_img

def show_image(imagen:np.ndarray, resultado:np.ndarray) -> np.ndarray:
    if imagen.shape [-1] < 3:
        return

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(121, projection= "3d")
    ax.plot_surface(imagen [:, :, 2], imagen [:, :, 1], imagen [:, :, 0],
                    facecolors=resultado/255.0)
    ax2 = fig.add_subplot(122, projection="3d")
    X, Y = np.meshgrid (np.arange(imagen.shape[0]), np.arange(imagen.shape[1]))
    ax2.plot_surface (X, Y, imagen [:, :, 0], facecolors = resultado/255.0)
    plt.show()

#test 1
if __name__ == "__main__":
    path = r"C:\Users\marco\Documents\images.jpg"

    if os.path.exists (path):
        imagen = cv2.imread (path, 1)
        imagen = cv2.cvtColor (imagen, cv2.COLOR_BGR2RGB)
        imagen = cv2.resize(imagen, (250, 250), cv2.INTER_AREA)
    else:
        imagen = np.random.randint (0, 255, (250,250), dtype= np.uint8)

    resultado = rgb_2_cielab_custom (imagen)
    show_image(resultado, imagen)