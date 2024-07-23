import pygame as pg
import sys

# Inicializar Pygame
pg.init()


#Pantalla o Ventana
w,h=(1000,600)
PANTALLA = pg.display.set_mode((w,h))
FPS = 30
RELOJ = pg.time.Clock()
# Colores
COLOR_VIDA = (0,255,0)  # Rojo
COLOR_FONDO_VIDA = (255,0,0)  # Blanco

# Variables de la vida del personaje
vida_maxima = 100
vida_actual = 50

def dibujar_barra_vida(x, y, vida, vida_max):
    # Dimensiones de la barra de vida
    ancho, alto = 200, 20
    fill = (vida / vida_max) * ancho
    borde = pg.Rect(25, 10, ancho, alto)
    fill_rect = pg.Rect(25, 10, fill, alto)
    
    pg.draw.rect(PANTALLA, COLOR_FONDO_VIDA, borde)
    pg.draw.rect(PANTALLA, COLOR_VIDA, fill_rect)
    pg.draw.rect(PANTALLA, (0,0,0), borde, 2)  # Dibuja el borde



#Fondo del juego
fondo=pg.image.load("Imagenes\\FondoJuego_resized.jpg").convert()

#Imagenes Movimiento
Mderecha=[pg.image.load('Personajes\\Personaje1\\Derecho1.png'),
          pg.image.load('Personajes\\Personaje1\\Derecho2.png'),
          pg.image.load('Personajes\\Personaje1\\Derecho3.png'),
          pg.image.load('Personajes\\Personaje1\\Derecho4.png')]

SaltoMovimiento= [pg.image.load('Personajes\\Personaje1\\Salto2.png'),
                  pg.image.load('Personajes\\Personaje1\\Salto3.png'),
                  pg.image.load('Personajes\\Personaje1\\Salto4.png')]

MIzquierda=[pg.image.load('Personajes\\Personaje1\\Izquierdo1.png'),
            pg.image.load('Personajes\\Personaje1\\Izquierdo2.png'),
            pg.image.load('Personajes\\Personaje1\\Izquierdo3.png'),
            pg.image.load('Personajes\\Personaje1\\Izquierdo4.png')]

framesAtaque = [pg.image.load('Personajes\\Personaje1\\Derecho1.png'),
                pg.image.load('Personajes\\Personaje1\\Ataque2.png'),
                pg.image.load('Personajes\\Personaje1\\Derecho1.png')]

Quieto = pg.image.load('Personajes\\Personaje1\\Derecho1.png')


#Variables
x=0
px=50
py=200
ancho = 40
velocidad = 10
velocidad_animacion = 50

#Variables de Salto
salto = False
#Altura del salto 
cuentaSalto = 10
#Variables de direccion
Derecha = False
Izquierda = False
Ataque = False
#Pasos
cuentaPasos = 0
indiceAtaque = 0
velocidadAtaque = 5

#Movimiento
def recargarPantalla():
    #Variables Globales
    global cuentaPasos
    global x

    #Fondo en movimiento
    x_relativa = x % fondo.get_rect().width
    PANTALLA.blit(fondo,(x_relativa - fondo.get_rect().width , 0))
    if x_relativa < w:
        PANTALLA.blit(fondo,(x_relativa,0))
    x-=1

    dibujar_barra_vida(50, 50, vida_actual, vida_maxima)

    # Contador de pasos actualizado para todas las direcciones
    if cuentaPasos + 1 >= 6:
        cuentaPasos = 0

    # Movimiento a la Izquierda
    if Izquierda:
        PANTALLA.blit(MIzquierda[cuentaPasos // 1 % len(MIzquierda)], (int(px), int(py)))
        cuentaPasos += 1
    
    elif Ataque:  # Si Ataque es True, asegúrate de que esta condición se refiera a si el personaje está atacando
        PANTALLA.blit(framesAtaque[cuentaPasos // 1 % len(framesAtaque)], (int(px), int(py)))
        cuentaPasos += 1

# Movimiento a la derecha
    elif Derecha:
        PANTALLA.blit(Mderecha[cuentaPasos // 1 % len(Mderecha)], (int(px), int(py)))
        cuentaPasos += 1

# Movimiento de Salto
    elif salto + 1 >=2 :
        PANTALLA.blit(SaltoMovimiento[cuentaPasos // 1 % len(SaltoMovimiento)], (int(px), int(py)))
        cuentaPasos += 1

#Movimiento estatico
    else: 
        PANTALLA.blit(Quieto, (int(px), int(py)))
    
    pg.display.update()


ejecuta  = True
#Bucle del Juego
while ejecuta:
    
    RELOJ.tick(FPS)
    
    #Bucle del Juego
    for event in pg.event.get():
        if event.type == pg.QUIT:
            ejecuta = False
    #Teclas presionadas
    keys = pg.key.get_pressed()

    #Tecla A-Movimiento a la Izquierda
    if keys[pg.K_a] and px > velocidad:
        px -= velocidad
        Izquierda = True
        Derecha = False
    
    elif keys[pg.K_v] and px > 0:
        px -= velocidad
        Ataque = True
        Izquierda = False 
        Derecha  = False
        

    #Tecla D-Movimiento a la Izquierda
    elif keys[pg.K_d] and px < 900  - velocidad - ancho:
        px += velocidad
        Izquierda = False
        Derecha = True
        Ataque = False
    #Personaje Quieto
    else:
        Izquierda = False
        Derecha = False
        cuentaPasos = 0
    #Tecla W-Salto
    if not (salto):
        if keys[pg.K_SPACE] :
            salto = True
            Izquierda = False
            derecha = False
            cuentaPasos = 0
    else:
        if cuentaSalto >= -10:
            py -= (cuentaSalto * abs(cuentaSalto)) * 0.5
            cuentaSalto -= 1
        else: 
            cuentaSalto = 10
            salto = False   

    recargarPantalla()

#Salida del Juego
pg.quit()
   
   
