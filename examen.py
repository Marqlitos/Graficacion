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
    gris = (60, 60, 60)    
    A = 50
    d = 2
    rad_px = 0.1
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

        x = px * rad_px
        y = int(H / 2 - A * math.sin(x))
        pantalla.fill(blanco)
        
        pg.draw.circle(pantalla, azul, (px, y), radio)
        
        pg.draw.circle(pantalla, verde, (px, y), radio)
        
        pg.display.flip()
        reloj.tick(30)
        
    pg.quit()

if __name__ == "__main__":
    main()