import pygame as pg

# Linea recta
def linea_recta(c1:tuple[int], c2:tuple[int]) -> list[tuple[int]] | None:
    if len(c1) != 2:
        return
    result = []
    
    # Lineas especificas
    if (c2[0] - c1[0]) == 0:
        if c2[1] > c1[1]:
            for y in range(c1[1], c2[1]):
                result.append((c1[0], y))
            return result
        else:
            for y in range(c2[1], c1[1]):
                result.append((c1[0], y))
            return result
    elif (c2[1] - c1[1]) == 0:
        if c2[0] < c1[0]:
            for x in range(c2[0], c1[0]):
                result.append((x, c1[1]))
            return result
        else:
            for x in range(c1[0], c2[0]):
                result.append((x, c1[1]))
            return result
    
    # Paso 2: Calcular la pendiente
    m = int((c2[1] - c1[1])/(c2[0] - c1[0]))
    
    # Paso 3: Calcular el bias
    b = c2[1] - m*c2[0]
    
    # Paso 4: Calcular los puntos de la linea
    
    for x in range(c1[0], c2[0]):
        y = m*x + b
        result.append((x, y))
        
    return result

def dibujar_triangulo(c1:tuple[int], c2:tuple[int], c3:tuple[int]) -> list[tuple[int]]:
    if not isinstance(c1, tuple):
        return

    rec_1 = linea_recta(c1, c2)
    rec_2 = linea_recta(c2, c3)
    rec_3 = linea_recta(c3, c1)

    return [rec_1, rec_2, rec_3]

# Dibujar un punto
def main() -> None:
    # Ajustes
    pg.init()
    W, H = 600, 400
    pantalla = pg.display.set_mode((W, H))
    clock = pg.time.Clock()
    ejec = True
    
    # Coordenadas para la linea
    c1 = (int(W/2) - 50, int(H/2))
    c2 = (300, 100)
    c3 = (350, 200)

    triangulo = dibujar_triangulo(c1, c2, c3)
    
    # Colores
    blanco = (255, 255, 255)
    negro = (0, 0, 0)
    
    
    pantalla.fill(negro)
    
    while ejec:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejec = False
        
        # Dibujar linea
        for tr in triangulo:
            for point in tr:
                pantalla.set_at(point, blanco)

        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()