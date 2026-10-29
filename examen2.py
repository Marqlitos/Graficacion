import pygame as pg
import numpy as np

def linea_recta(c1: tuple[int, int], c2: tuple[int, int]) -> list[tuple[int, int]] | None:
    if len(c1) != 2 or len(c2) != 2:
        return None

    if (c2[0] - c1[0]) == 0:
        result = []
        paso = 1 if c2[1] >= c1[1] else -1
        for y in range(c1[1], c2[1] + paso, paso):
            result.append((c1[0], y))
        return result

    if (c2[1] - c1[1]) == 0:
        result = []
        paso = 1 if c2[0] >= c1[0] else -1
        for x in range(c1[0], c2[0] + paso, paso):
            result.append((x, c1[1]))
        return result

    m = (c2[1] - c1[1]) / (c2[0] - c1[0])
    b = c2[1] - m * c2[0]
    result = []
    x_inicial = min(c1[0], c2[0])
    x_final = max(c1[0], c2[0])

    for x in range(x_inicial, x_final + 1):
        y = int(round(m * x + b))
        result.append((x, y))
    return result

def dibujar_circulo(a: float, b: float, r: int = 1) -> list[tuple[int, int]]:
    result = []
    for x in range(int(a - r), int(a + r) + 1):
        raiz = (r ** 2) - (x - a) ** 2
        if raiz >= 0:
            result.append((x, int(round(b + np.sqrt(raiz)))))
            result.append((x, int(round(b - np.sqrt(raiz)))))
    return result


def main() -> None:
    pg.init()
    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    clock = pg.time.Clock()
    ejec = True

    pos1 = (200, 300)
    pos2 = (250, 300)
    cc1 = (300, 250)
    radio = 60
    negro = (0, 0, 0)
    blanco = (255, 255, 255)
    puntos_linea = linea_recta(pos1, pos2)
    puntos_circulo = dibujar_circulo(cc1[0], cc1[1], radio)
    pantalla.fill(negro)

    if puntos_linea:
        for p in puntos_linea:
            if 0 <= p[0] < W and 0 <= p[1] < H:
                pantalla.set_at(p, blanco)

    for p in puntos_circulo:
        if 0 <= p[0] < W and 0 <= p[1] < H:
            pantalla.set_at(p, blanco)

    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        pg.display.flip()
        clock.tick(60)
    pg.quit()


if __name__ == "__main__":
    main()