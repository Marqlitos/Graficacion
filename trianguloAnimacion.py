
import pygame as pg
import math

def main() -> None:
    pg.init()
    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    reloj = pg.time.Clock()
    ejec = True

    blanco = (255, 255, 255)
    azul = (75, 155, 255)
    verde = (75, 155, 35)

    radio = 4
    velocidad = 2

    # Vértices del triángulo
    puntos = [
        (50, 350),
        (300, 50),
        (550, 350)
    ]

    lado = 0
    progreso = 0.0

    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        # Lado actual del triángulo
        inicio = puntos[lado]
        fin = puntos[(lado + 1) % 3]

        dx = fin[0] - inicio[0]
        dy = fin[1] - inicio[1]
        distancia = math.hypot(dx, dy)

        progreso += velocidad / distancia

        if progreso >= 1:
            progreso = 0
            lado = (lado + 1) % 3

        # Posición de la pelota sobre el lado
        x = int(inicio[0] + dx * progreso)
        y = int(inicio[1] + dy * progreso)

        pantalla.fill(blanco)

        # Dibujar la pelota
        pg.draw.circle(pantalla, azul, (x, y), radio)

        pg.display.flip()
        reloj.tick(30)

    pg.quit()

if __name__ == "__main__":
    main()
