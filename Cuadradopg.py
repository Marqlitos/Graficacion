
import pygame as pg

# Línea recta
def linea_recta(c1: tuple[int, int], c2: tuple[int, int]) -> list[tuple[int, int]]:
    result = []

    x1, y1 = c1
    x2, y2 = c2

    # Calcular la diferencia entre coordenadas
    dx = x2 - x1
    dy = y2 - y1

    # Determinar la cantidad de pasos
    pasos = max(abs(dx), abs(dy))

    # Si los puntos son iguales
    if pasos == 0:
        return [c1]

    # Calcular el incremento en cada eje
    inc_x = dx / pasos
    inc_y = dy / pasos

    # Generar los puntos de la línea
    for i in range(pasos + 1):
        x = round(x1 + inc_x * i)
        y = round(y1 + inc_y * i)
        result.append((x, y))

    return result


# Dibujar un cuadrado o rectángulo
def dibujar_cuadrado(c1: tuple[int, int], c2: tuple[int, int]) -> list[list[tuple[int, int]]]:

    # Calcular las otras dos esquinas
    c3 = (c1[0], c2[1])
    c4 = (c2[0], c1[1])

    # Dibujar los cuatro lados
    rec_1 = linea_recta(c1, c3)
    rec_2 = linea_recta(c1, c4)
    rec_3 = linea_recta(c4, c2)
    rec_4 = linea_recta(c2, c3)

    return [rec_1, rec_2, rec_3, rec_4]


# Programa principal
def main() -> None:
    # Ajustes
    pg.init()
    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    pg.display.set_caption("Dibujar un cuadrado")
    clock = pg.time.Clock()
    ejec = True

    # Coordenadas de las esquinas opuestas
    c1 = (300, 200)
    c2 = (500, 100)

    cuadrado = dibujar_cuadrado(c1, c2)

    # Colores
    blanco = (255, 255, 255)
    negro = (0, 0, 0)

    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        pantalla.fill(negro)

        # Dibujar los cuatro lados
        for tr in cuadrado:
            for point in tr:
                pantalla.set_at(point, blanco)

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
