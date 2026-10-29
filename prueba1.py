import pygame as pg
import math

def main() -> None:
    pg.init()
    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    clock = pg.time.Clock()
    ejec = True

    negro = (0, 0, 0)
    verde = (75, 155, 35)
    gris = (60, 60, 60)

    A = 50
    d = 2
    rad_por_px = 0.1
    radio = 4

    px = 0

    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        px += d

        if px >= W:
            px = W
            d = -d
        elif px <= 0:
            px = 0
            d = -d

        x = px * rad_por_px
        y = int(H / 2 - A * math.sin(x))

        pantalla.fill(negro)
        pg.draw.circle(pantalla, verde, (px, y), radio)

        pg.display.flip()
        clock.tick(30)

    pg.quit()

if __name__ == "__main__":
    main()