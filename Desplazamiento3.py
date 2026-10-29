import pygame as pg
import time
import random
import math

def main() -> None:
    #ajuste
    pg.init()
    W,H = 600, 400
    pantalla = pg.display.set_mode((W,H))
    clock = pg.time.Clock()
    ejec = True
    
    #Coordenada
    c1 = (int(W/2), int (H/2)) #Es el origen
    c2 = (int(W/2) + 50, int(H/2)) #Punto 2 completa la linea
    
    #Longitud y angulo
    l = math.sqrt((c1[0]-c2[0])**2 + (c2[1]-c1[1])**2)
    angulo = 0
    
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
        
        #d2 = random.randint(-10, 10)        
        
        #animacion
            
        angulo += 50
        angulo %= 360
            
        pg.draw.line(pantalla, color=linea, start_pos=c1, end_pos= c2,
                     width=5)
        pg.draw.circle(pantalla,color=(255,0,0), center=c1,
                       radius=4)
        
        time.sleep(0.03)
        
        x = c1 [0] + l*math.cos(math.radians(angulo))
        y = c1 [1] - l*math.sin(math.radians(angulo))
        
        pg.display.flip()
        clock.tick(120)
        pantalla.fill(negro)
    
    pg.quit()

if __name__ == "__main__":
    main()
    
#Tarea lo mismo pero en triangulo
