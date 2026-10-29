
import pygame as pg

# Línea recta
def linea_recta(c1: tuple[int], c2: tuple[int]) -> list[tuple[int]] | None:
    if len(c1) != 2 or len(c2) != 2:
        return

    result = []

    # Líneas verticales
    if c2[0] - c1[0] == 0:
        for y in range(min(c1[1], c2[1]), max(c1[1], c2[1]) + 1):
            result.append((c1[0], y))
        return result

    # Líneas horizontales
    elif c2[1] - c1[1] == 0:
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


# Dibujar el plano cartesiano
def dibujar_plano(W: int, H: int):
    lineas = []

    # Centro de la pantalla
    centro_x = W // 2
    centro_y = H // 2

    # Eje X horizontal
    eje_x = linea_recta((0, centro_y), (W - 1, centro_y))
    lineas.append((eje_x, (255, 255, 255)))

    # Eje Y vertical
    eje_y = linea_recta((centro_x, 0), (centro_x, H - 1))
    lineas.append((eje_y, (255, 255, 255)))

    # Cuadrícula vertical
    for x in range(0, W, 20):
        if x != centro_x:
            linea = linea_recta((x, 0), (x, H - 1))
            lineas.append((linea, (50, 50, 50)))

    # Cuadrícula horizontal
    for y in range(0, H, 20):
        if y != centro_y:
            linea = linea_recta((0, y), (W - 1, y))
            lineas.append((linea, (50, 50, 50)))

    return lineas


# Programa principal
def main() -> None:
    # Ajustes
    pg.init()

    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    pg.display.set_caption("Plano cartesiano")

    clock = pg.time.Clock()
    ejec = True

    # Colores
    negro = (0, 0, 0)

    # Crear el plano cartesiano
    plano = dibujar_plano(W, H)

    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        pantalla.fill(negro)

        # Dibujar todas las líneas
        for puntos, color in plano:
            for point in puntos:
                pantalla.set_at(point, color)

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
