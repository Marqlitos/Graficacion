
import pygame as pg
import math
import numpy as np

# Línea recta
def linea_recta(c1: tuple[int], c2: tuple[int]) -> list[tuple[int]] | None:
    if len(c1) != 2:
        return

    result = []

    # Líneas verticales
    if (c2[0] - c1[0]) == 0:
        for y in range(min(c1[1], c2[1]), max(c1[1], c2[1]) + 1):
            result.append((c1[0], y))
        return result

    # Líneas horizontales
    elif (c2[1] - c1[1]) == 0:
        for x in range(min(c1[0], c2[0]), max(c1[0], c2[0]) + 1):
            result.append((x, c1[1]))
        return result

    # Calcular la pendiente
    m = (c2[1] - c1[1]) / (c2[0] - c1[0])

    # Calcular el bias
    b = c2[1] - m * c2[0]

    # Calcular los puntos de la línea
    for x in range(min(c1[0], c2[0]), max(c1[0], c2[0]) + 1):
        y = round(m * x + b)
        result.append((x, y))

    return result


# Dibujar un círculo
def dibujar_circulo(a: int, b: int, r: int = 50) -> list[tuple[int, int]]:
    puntos = []

    # Recorrer las coordenadas X del círculo
    for x in range(a - r, a + r + 1):
        raiz = r**2 - (x - a)**2

        if raiz >= 0:
            y = int(np.sqrt(raiz))

            # Parte superior e inferior del círculo
            puntos.append((x, b - y))
            puntos.append((x, b + y))

    return puntos


# Programa principal
def main() -> None:
    # Ajustes
    pg.init()

    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    pg.display.set_caption("Dibujar un círculo")

    clock = pg.time.Clock()
    ejec = True

    # Centro del círculo y radio
    a = 200
    b = 200
    r = 50

    circulo = dibujar_circulo(a, b, r)

    # Colores
    blanco = (255, 255, 255)
    negro = (0, 0, 0)

    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        pantalla.fill(negro)

        # Dibujar los puntos del círculo
        for point in circulo:
            pantalla.set_at(point, blanco)

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()