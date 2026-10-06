import pygame as pg

#Linea Recta
def linea_recta(c1:tuple[int], c2:tuple[int]) -> list[tuple[int]] | None:
    if len (c1) !=2:
        return
    
    if (c2 [0] - c1[0]) == 0:
        result = []
        for y in range(c2[1], c1[1]):
            result.append((c1[0], y))
        return result
    
    m = (c2[1] - c2[1]/(c2[0] - c1[0]))
    b = c2[1] - m*c2[0]
    
    result = []
    
    for x in range (c1[0], c2[0]):
        y = m*x + b
        result.append((x,y))
    return result
    
def main() -> None:
    # Ajustes
    pg.init()
    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    clock = pg.time.Clock()
    ejec = True

    c1 = (int(W/2), int(H/2))
    c2 = (300, 100)

    # Colores
    blanco = (255, 255, 255)
    negro = (0, 0, 0)

    pantalla.fill(negro)

    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False

        # Dibujar
        points = linea_recta(c1, c2)
        for point in points:
            pantalla.set_at(point, blanco)
            
    pg.display.flip()
    clock.tick(60)
    pg.quit()


if __name__ == "__main__":
    main()
