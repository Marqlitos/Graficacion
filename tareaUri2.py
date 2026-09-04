import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def pixel_rgb_to_ycbcr(r, g, b):
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    y_norm  =  0.299 * r_norm + 0.587 * g_norm + 0.114 * b_norm
    cb_norm = -0.1687 * r_norm - 0.3313 * g_norm + 0.5 * b_norm + 0.5
    cr_norm =  0.5 * r_norm - 0.4187 * g_norm - 0.0813 * b_norm + 0.5

    y  = round(y_norm * 255)
    cb = round(cb_norm * 255)
    cr = round(cr_norm * 255)

    return y, cb, cr

r, g, b = 255, 128, 64
y, cb, cr = pixel_rgb_to_ycbcr(r, g, b)
print(f"Y: {y}, Cb: {cb}, Cr: {cr}")
