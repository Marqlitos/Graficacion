import pygame as pg
import time

def main() -> None:
    #ajuste
    pg.init()
    W,H = 600, 400
    pantalla = pg.display.set_mode((W,H))
    clock = pg.time.Clock()
    ejec = True
    
    #Coordenada
    c1 = (int(W/2), int (H/2)) #Es el origen
    radio = 4
    
    #velocidad
    d = 5
    
    #colores
    negro= (0, 0 , 0)
    raro = (75, 155, 255)
    
    pantalla.fill(negro)
    
    #ejecucion
    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False
                
        #Condicion para rebotar
        if c1[0] + radio >= W:
            d = -d
        elif c1[0] - radio <= 0:
            d = -d
        
        #animacion
        pg.draw.circle(pantalla, color=raro, center=c1, radius=radio)
        c1 = (c1[0] + d, c1[1])
        time.sleep(0.01)
    
        pg.display.flip()
        clock.tick(120)
        pantalla.fill(negro)
    
    pg.quit()

if __name__ == "__main__":
    main()