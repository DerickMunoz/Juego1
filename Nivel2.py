import pygame as pg
import sys
import random

pg.init()

# Pantalla o Ventana
w, h = (1000, 600)
PANTALLA = pg.display.set_mode((w, h))
FPS = 50
RELOJ = pg.time.Clock()

# Colores
COLOR_VIDA = (0, 255, 0)  # Verde
COLOR_FONDO_VIDA = (255, 0, 0)  # Rojo

# Variables de vida
vida_maxima = 100
vida_actual = vida_maxima
vida_maxima_spider = 5
vida_actual_spider = vida_maxima_spider
velocidad = 5

# Cargar imágenes
fondo = pg.image.load("Imagenes\\FondoJuego_resized.jpg").convert()
Mderecha = [pg.image.load(f'Personajes\\Personaje1\\Derecho{i}.png') for i in range(1, 5)]
MIzquierda = [pg.image.load(f'Personajes\\Personaje1\\Izquierdo{i}.png') for i in range(1, 5)]
framesAtaque = [pg.image.load(f'Personajes\\Personaje1\\Derecho1.png'), pg.image.load(f'Personajes\\Personaje1\\Ataque2.png')]
animacion_objeto = [pg.image.load('Personajes\\Personaje1\\Animacion Ataque.png') for _ in range(5)]
Quieto = pg.image.load('Personajes\\Personaje1\\Derecho1.png')
FramesSpider = [pg.image.load(f'Personajes\\Enemigo1\\Spider{i}.png') for i in range(1, 4)]

class BarraVida:
    def __init__(self, x, y, ancho=200, alto=20):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto

    def dibujar(self, pantalla, vida, vida_max):
        fill = (vida / vida_max) * self.ancho
        borde = pg.Rect(self.x, self.y, self.ancho, self.alto)
        fill_rect = pg.Rect(self.x, self.y, fill, self.alto)
        pg.draw.rect(pantalla, COLOR_FONDO_VIDA, borde)
        pg.draw.rect(pantalla, COLOR_VIDA, fill_rect)
        pg.draw.rect(pantalla, (0, 0, 0), borde, 2)

class Spider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cuentaPasos = 0
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.velocidad_animacion = 30  # Controla la velocidad de la animación
        self.contador_animacion = 0
        self.ancho = 200
        self.alto = 350
        self.rect = pg.Rect(x, y, self.ancho, self.alto)
        self.fragmentos = []

    def actualizar_rect(self):
        self.rect = pg.Rect(self.x, self.y, self.ancho, self.alto)
    
    def lanzar_fragmento(self):
        fragmento = Fragmento(self.x, self.y)
        self.fragmentos.append(fragmento)

    def mover(self):
        self.x += self.direccion
        if self.x <= 0 or self.x >= 800 - self.ancho:
            self.direccion *= -1

    def dibujar(self, pantalla):
        pantalla.blit(FramesSpider[self.cuentaPasos // 1 % len(FramesSpider)], (self.x, self.y))
        self.contador_animacion += 1
        if self.contador_animacion >= self.velocidad_animacion:
            self.cuentaPasos += 1
            self.contador_animacion = 0
        if self.cuentaPasos >= len(FramesSpider):
            self.cuentaPasos = 0

    def obtener_rect(self):
        return self.rect

    def actualizar_fragmentos(self, personaje_principal):
        for fragmento in self.fragmentos:
            fragmento.mover()
            if fragmento.colisiona_con(personaje_principal.rect):
                personaje_principal.vida -= 10  # Reducir la vida del personaje principal
                self.fragmentos.remove(fragmento)

class Fragmento:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad_x = random.randint(-5, 5)
        self.velocidad_y = random.randint(-5, 5)
        self.rect = pg.Rect(self.x, self.y, 10, 10)

    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.rect.topleft = (self.x, self.y)

    def colisiona_con(self, otro_rect):
        return self.rect.colliderect(otro_rect)

class PersonajePrincipal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 40
        self.alto = 64
        self.vida = 100
        self.velocidad = 5
        self.rect = pg.Rect(x, y, self.ancho, self.alto)

    def mover(self, direccion):
        if direccion == "izquierda":
            self.x -= self.velocidad
        elif direccion == "derecha":
            self.x += self.velocidad
        elif direccion == "arriba":
            self.y -= self.velocidad
        self.actualizar_rect()

    def actualizar_rect(self):
        self.rect.topleft = (self.x, self.y)

class ObjetoColision:
    def __init__(self, x, y, ancho, alto, velocidad):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.cuentaPasos = 0
        self.contador_animacion = 0

    def mover(self):
        self.x += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(animacion_objeto[self.cuentaPasos // 1 % len(animacion_objeto)], (self.x, self.y))
        self.contador_animacion += 1
        if self.contador_animacion >= 5:
            self.cuentaPasos += 1
            self.contador_animacion = 0
        if self.cuentaPasos >= len(animacion_objeto):
            self.cuentaPasos = 0

    def obtener_rect(self):
        return pg.Rect(self.x, self.y, self.ancho, self.alto)

def detectar_colision(rect1, rect2):
    return rect1.colliderect(rect2)

def recargar_pantalla():
    global cuentaPasos, x

    # Fondo en movimiento
    x_relativa = x % fondo.get_rect().width
    PANTALLA.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < w:
        PANTALLA.blit(fondo, (x_relativa, 0))
    x -= 1

    barra_vida.dibujar(PANTALLA, vida_actual, vida_maxima)
    barra_vida_spider.dibujar(PANTALLA, vida_actual_spider, vida_maxima_spider)
    spider.dibujar(PANTALLA)

    for objeto in objetos_colision:
        objeto.dibujar(PANTALLA)

    if cuentaPasos + 1 >= 6:
        cuentaPasos = 0

    if Izquierda:
        PANTALLA.blit(MIzquierda[cuentaPasos // 1 % len(MIzquierda)], (px, py))
        cuentaPasos += 1
    elif Derecha:
        PANTALLA.blit(Mderecha[cuentaPasos // 1 % len(Mderecha)], (px, py))
        cuentaPasos += 1
    elif Ataque:
        PANTALLA.blit(framesAtaque[cuentaPasos // 1 % len(framesAtaque)], (px, py))
        cuentaPasos += 1
    else:
        PANTALLA.blit(Quieto, (px, py))

    pg.display.update()

# Variables del juego
x = 0
px, py = 50, 200
salto = False
cuentaSalto = 10
Derecha = False
Izquierda = False
Ataque = False
cuentaPasos = 0

# Crear instancias
spider = Spider(650, 120)
personaje_principal = PersonajePrincipal(50, 200)
barra_vida = BarraVida(50, 50)
barra_vida_spider = BarraVida(750, 25)
objetos_colision = []

# Bucle principal del juego
ejecuta = True
while ejecuta:
    RELOJ.tick(FPS)

    if vida_actual <= 0:
        fuente = pg.font.Font(None, 74)
        texto = fuente.render("Has muerto", True, (255, 0, 0))
        PANTALLA.blit(texto, (PANTALLA.get_width() // 2 - texto.get_width() // 2, PANTALLA.get_height() // 2 - texto.get_height() // 2))
        pg.display.flip()
        pg.time.delay(2000)
        ejecuta = False
        pg.quit()
        sys.exit()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            ejecuta = False

    for objeto in objetos_colision:
        objeto.mover()
        if detectar_colision(objeto.obtener_rect(), spider.obtener_rect()):
            objetos_colision.remove(objeto)
            vida_actual_spider -= 1
        if objeto.x >= w:
            objetos_colision.remove(objeto)

    if vida_actual_spider <= 0:
        fuente = pg.font.Font(None, 74)
        texto = fuente.render("Has ganado", True, (255, 255, 0))
        PANTALLA.blit(texto, (PANTALLA.get_width() // 2 - texto.get_width() // 2, PANTALLA.get_height() // 2 - texto.get_height() // 2))
        pg.display.flip()
        pg.time.delay(2000)
        ejecuta = False
        pg.quit()
        sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and px > velocidad:
        px -= velocidad
        Izquierda = True
        Derecha = False
        Ataque = False
    elif keys[pg.K_RIGHT] and px < 1000 - velocidad - 30:
        px += velocidad
        Derecha = True
        Izquierda = False
        Ataque = False
    else:
        Derecha = False
        Izquierda = False
        cuentaPasos = 0
    if not salto:
        if keys[pg.K_SPACE]:
            salto = True
            Derecha = False
            Izquierda = False
            Ataque = True
            cuentaPasos = 0
            objeto = ObjetoColision(px + 30, py + 30, 30, 30, 8)
            objetos_colision.append(objeto)
    else:
        if cuentaSalto >= -10:
            direccion = 1
            if cuentaSalto < 0:
                direccion = -1
            py -= (cuentaSalto ** 2) * 0.25 * direccion
            cuentaSalto -= 1
        else:
            salto = False
            cuentaSalto = 10

    spider.mover()
    spider.actualizar_fragmentos(personaje_principal)
    recargar_pantalla()

pg.quit()
