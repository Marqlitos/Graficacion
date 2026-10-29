import pygame as pg
import time
import random

def main() -> None:
    #ajuste
    pg.init()
    W,H = 600, 400
    pantalla = pg.display.set_mode((W,H))
    clock = pg.time.Clock()
    ejec = True
    
    #Coordenada
    c1 = (int(W/2), int (H/2)) #Es el origen
    c2 = (int(W/2) + 50, int(H/2) + 50) #Punto 2 completa la linea
    
    #velocidad
    d = 5
    d2 = 7
    
    #colores
    negro= (0, 0 , 0)
    linea = (75, 155, 35)
    
    pantalla.fill(negro)
    
    #ejecucion
    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False
                
        #Condicion para rebotar
        #if c1[0] - radio >= W:
         #   d = -d
        #elif c1[0] + radio <= 0:
        #    d = -d
        
        d2 = random.randint(-10, 10)        
        
        #animacion
        if c1[0] <= 0 or c2[0] >= W:
            d = -d
        elif c1[1] <= 0 or c2[1] >= W:
            d2 = -d2
            
        pg.draw.line(pantalla, color=linea, start_pos=c1, end_pos= c2,
                     width=5)
        time.sleep(0.03)
        c1 = (c1[0] + d, c1[1] + d2)
        c2 = (c2[0] + d, c2[1] + d2)
        
        pg.display.flip()
        clock.tick(120)
        pantalla.fill(negro)
    
    pg.quit()

if __name__ == "__main__":
    main()
    
#Tarea lo mismo pero en triangulo