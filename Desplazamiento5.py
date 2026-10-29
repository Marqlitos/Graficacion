import pygame as pg
import math

def main() -> None:
    # Ajustes
    pg.init()
    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    pg.display.set_caption("Colisión de círculos")

    clock = pg.time.Clock()
    ejec = True

    # Coordenadas
    c1 = (W // 2, H // 2)
    radio_orbita = 120
    radio_circulo = 5

    # Ángulos
    angulo_1 = 0.0
    angulo_2 = 180.0

    # Velocidades
    vel_1 = 2.0
    vel_2 = -2.0

    # Colores
    negro = (0, 0, 0)
    color_c1 = (75, 155, 235)
    color_c2 = (235, 155, 75)
    ref_color = (255, 35, 150)
    circulo_guia = (50, 50, 50)
    color_impacto = (255, 50, 50)

    # Control de colisión
    colision_anterior = False

    # Ejecución
    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        pantalla.fill(negro)

        # Convertir ángulos a radianes
        rad_1 = math.radians(angulo_1)
        rad_2 = math.radians(angulo_2)

        # Posición del primer círculo
        x1 = c1[0] + radio_orbita * math.cos(rad_1)
        y1 = c1[1] - radio_orbita * math.sin(rad_1)
        pos_1 = (x1, y1)

        # Posición del segundo círculo
        x2 = c1[0] + radio_orbita * math.cos(rad_2)
        y2 = c1[1] - radio_orbita * math.sin(rad_2)
        pos_2 = (x2, y2)

        # Calcular distancia
        distancia = math.hypot(x2 - x1, y2 - y1)
        distancia_minima = radio_circulo * 2

        # Detectar colisión
        colision = distancia <= distancia_minima

        # Invertir dirección al chocar
        if colision and not colision_anterior:
            vel_1 *= -1
            vel_2 *= -1

        colision_anterior = colision

        # Actualizar ángulos
        angulo_1 = (angulo_1 + vel_1) % 360
        angulo_2 = (angulo_2 + vel_2) % 360

        # Dibujar órbita
        pg.draw.circle(
            pantalla, circulo_guia, c1,
            radio_orbita, width=1
        )

        # Dibujar centro
        pg.draw.circle(pantalla, ref_color, c1, 5)

        # Colores según colisión
        c1_color_actual = color_impacto if colision else color_c1
        c2_color_actual = color_impacto if colision else color_c2

        # Dibujar círculos
        pg.draw.circle(
            pantalla, c1_color_actual, pos_1, radio_circulo
        )

        pg.draw.circle(
            pantalla, c2_color_actual, pos_2, radio_circulo
        )

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
    