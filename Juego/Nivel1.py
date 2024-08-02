import pygame as pg
import sys
import random



def main():    
    import pygame as pg
    import sys
    import random

    pg.init()


    #Pantalla o Ventana
    w,h=(1000,600)
    PANTALLA = pg.display.set_mode((w,h))
    FPS = 50
    RELOJ = pg.time.Clock()
    # Colores
    COLOR_VIDA = (0,255,0)  # Rojo
    COLOR_FONDO_VIDA = (255,0,0)  # Blanco

    # Variables de vida
    vida_maxima = 100
    vida_actual = 100
    # Variables de vida de Spider
    vida_maxima_spider = 5
    vida_actual_spider = vida_maxima_spider


    def detectar_colision(rect1, rect2):
        return rect1.colliderect(rect2)

    def dibujar_barra_vida(x, y, vida, vida_max):
        # Dimensiones de la barra de vida
        ancho, alto = 200, 20
        fill = (vida / vida_max) * ancho
        borde = pg.Rect(25, 10, ancho, alto)
        fill_rect = pg.Rect(25, 10, fill, alto)
        
        pg.draw.rect(PANTALLA, COLOR_FONDO_VIDA, borde)
        pg.draw.rect(PANTALLA, COLOR_VIDA, fill_rect)
        pg.draw.rect(PANTALLA, (0,0,0), borde, 2)  # Dibuja el borde



    def dibujar_barra_vidaSpider(x, y, vida_actual, vida_maxima):
        largo_barra = 200
        ancho_barra = 20
        relleno = (vida_actual / vida_maxima) * largo_barra
        borde = pg.Rect(x, y, largo_barra, ancho_barra)
        relleno = pg.Rect(x, y, relleno, ancho_barra)
        pg.draw.rect(PANTALLA, (0, 255, 0), relleno)
        pg.draw.rect(PANTALLA, (255, 255, 255), borde, 2)

    class Spider:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.cuentaPasos = 0
            self.direccion = 1  # 1 para derecha, -1 para izquierda
            self.velocidad_animacion = 30  # Controla la velocidad de la animación
            self.contador_animacion = 0
            self.ancho = 200  # Asume que la imagen tiene 64 píxeles de ancho
            self.alto = 350  # Asume que la imagen tiene 64 píxeles de alto
            self.rect = pg.Rect(x, y, ancho, alto)
            self.fragmentos = []

        def actualizar_rect(self):
            self.rect = pg.Rect(self.x, self.y, self.ancho, self.alto)
        
        def lanzar_fragmento(self):
            fragmento = Fragmento(self.x, self.y)
            self.fragmentos.append(fragmento)

        def mover(self):
            # Movimiento simple de izquierda a derecha
            self.x += self.direccion
            if self.x <= 0 or self.x >= 800 - 64:  # Asume que la imagen tiene 64 píxeles de ancho
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
            return pg.Rect(self.x, self.y, self.ancho, self.alto)
        def actualizar_fragmentos(self, personaje_principal):
            for fragmento in self.fragmentos:
                fragmento.mover()
                if fragmento.colisiona_con(personaje_principal):
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
            self.rect = pg.Rect(self.x, self.y, 10, 10)

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
            self.rect = pg.Rect(self.x, self.y, self.ancho, self.alto)

        def obtener_rect(self):
            return self.rect

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
            if self.contador_animacion >= 5:  # Ajusta la velocidad de la animación según sea necesario
                self.cuentaPasos += 1
                self.contador_animacion = 0
            if self.cuentaPasos >= len(animacion_objeto):
                self.cuentaPasos = 0

        def obtener_rect(self):
            return pg.Rect(self.x, self.y, self.ancho, self.alto)



    #Fondo del juego
    x = 100
    fondo=pg.image.load("Imagenes\\FondoJuego_resized.jpg").convert()

    #Personaje 1
    #Imagenes Movimiento
    Mderecha=[pg.image.load('Personajes\\Personaje1\\Derecho1.png'),
            pg.image.load('Personajes\\Personaje1\\Derecho2.png'),
            pg.image.load('Personajes\\Personaje1\\Derecho3.png'),
            pg.image.load('Personajes\\Personaje1\\Derecho4.png')]

    SaltoMovimiento= [pg.image.load('Personajes\\Personaje1\\Salto4.png'),]

    MIzquierda=[pg.image.load('Personajes\\Personaje1\\Izquierdo1.png'),
                pg.image.load('Personajes\\Personaje1\\Izquierdo2.png'),
                pg.image.load('Personajes\\Personaje1\\Izquierdo3.png'),
                pg.image.load('Personajes\\Personaje1\\Izquierdo4.png')]

    framesAtaque = [pg.image.load('Personajes\\Personaje1\\Derecho1.png'),
                    pg.image.load('Personajes\\Personaje1\\Ataque2.png'),
                    pg.image.load('Personajes\\Personaje1\\Derecho1.png')]
    animacion_objeto = [pg.image.load(f'Personajes\Personaje1\Animacion Ataque.png') for i in range(1, 6)]

    Quieto = pg.image.load('Personajes\\Personaje1\\Derecho1.png')

    #Spider
    FramesSpider = [pg.image.load('Personajes\Enemigo1\Spider1.png'),
                pg.image.load('Personajes\Enemigo1\Spider2.png'),
                pg.image.load('Personajes\Enemigo1\Spider3.png'),]
    #Variables
    x = 100
    px=50
    py=200
    ancho = 40
    alto = 64
    velocidad = 10
    velocidad_animacion =400 
    # Crear una instancia del personaje Spider
    spider = Spider(650, 120)
    personaje_principal = PersonajePrincipal(50, 200)
    otro_objeto = pg.Rect(120, 120, 30, 30)
    objetos_colision = []
    ancho, alto = 64, 64

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
    cuentaPasos = 0

    #Movimiento
    def recargarPantalla(x, fondo):
        global cuentaPasos  # Declarar cuentaPasos como global si es necesario
        x_relativa = x % fondo.get_rect().width
        
        PANTALLA.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
        if x_relativa < w:
            PANTALLA.blit(fondo, (x_relativa, 0))
        x -= 1

        # Inicializar cuentaPasos si no está inicializada
        if 'cuentaPasos' not in globals():
            cuentaPasos = 0

        if cuentaPasos + 1 >= 6:
            cuentaPasos = 0
        else:
            cuentaPasos += 1

        dibujar_barra_vida(50, 50, vida_actual, vida_maxima)
        dibujar_barra_vidaSpider(750, 25, vida_actual_spider, vida_maxima_spider)  # Barra de vida de Spider
        spider.dibujar(PANTALLA)
        for objeto in objetos_colision:
            objeto.dibujar(PANTALLA)

        # Contador de pasos actualizado para todas las direcciones
        if cuentaPasos + 1 >= 6:
            cuentaPasos = 0

        # Movimiento a la Izquierda
        if Izquierda:
            PANTALLA.blit(MIzquierda[cuentaPasos // 1 % len(MIzquierda)], (int(px), int(py)))
            cuentaPasos += 1
        elif Derecha:
            PANTALLA.blit(Mderecha[cuentaPasos // 1 % len(Mderecha)], (int(px), int(py)))
            cuentaPasos += 1
        elif Ataque:  # Si Ataque es True, asegúrate de que esta condición se refiera a si el personaje está atacando
            PANTALLA.blit(framesAtaque[cuentaPasos // 1 % len(framesAtaque)], (int(px), int(py)))
            cuentaPasos += 1
        else:
            PANTALLA.blit(Quieto, (int(px), int(py)))

        pg.display.update()

    # Variable para controlar el bucle del juego
    ejecuta = True

    # Bucle principal del juego
    while ejecuta:
        RELOJ.tick(FPS)
        # Actualizar el rectángulo de colisión del Spider
        spider.actualizar_rect()

        if vida_actual <= 0:
            
            print("Has muerto")
            # Mostrar mensaje en pantalla
            fuente = pg.font.Font(None, 74)
            texto = fuente.render("Has muerto", True, (255, 0, 0))
            PANTALLA.blit(texto, (PANTALLA.get_width() // 2 - texto.get_width() // 2, PANTALLA.get_height() // 2 - texto.get_height() // 2))
            pg.display.flip()
            pg.time.wait(3000)  # Esperar 3 segundos antes de cerrar
            ejecuta = False
        elif vida_actual_spider <= 0:
            
            print("Has ganado")
            # Mostrar mensaje en pantalla
            fuente = pg.font.Font(None, 74)
            texto = fuente.render("Has ganado", True, (0, 255, 0))
            PANTALLA.blit(texto, (PANTALLA.get_width() // 2 - texto.get_width() // 2, PANTALLA.get_height() // 2 - texto.get_height() // 2))
            pg.display.flip()
            pg.time.wait(3000)  # Esperar 3 segundos antes de cerrar
            ejecuta = False 
        # Bucle del Juego
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejecuta = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_v and Derecha == False and Izquierda == False :  # Cambiado de K_SPACE a K_v
                    # Crear un nuevo objeto de colisión
                    nuevo_objeto = ObjetoColision(px + ancho, py + alto // 4 + 40, 10, 40, 10)
                    objetos_colision.append(nuevo_objeto)
        
        teclas = pg.key.get_pressed()
        if teclas[pg.K_a]:
            personaje_principal.mover("izquierda")
        if teclas[pg.K_d]:
            personaje_principal.mover("derecha")
        if teclas[pg.K_SPACE]:
            personaje_principal.mover("arriba")  

        spider.actualizar_rect()   
        # Lógica para lanzar fragmentos de manera aleatoria
        if random.randint(0, 100) < 5:  # 5% de probabilidad de lanzar un fragmento en cada iteración
            spider.lanzar_fragmento() 
        # Actualizar y mover los fragmentos
        spider.actualizar_fragmentos(personaje_principal)      

        # Teclas presionadas
        keys = pg.key.get_pressed()
        # Tecla A-Movimiento a la Izquierda
        if keys[pg.K_a] and px > velocidad:
            px -= velocidad
            Izquierda = True
            Derecha = False

        # Tecla D-Movimiento a la Derecha
        elif keys[pg.K_d] and px < 900 - velocidad - ancho:
            px += velocidad
            Izquierda = False
            Derecha = True
            Ataque = False
            #Tecla Ataque
        elif keys[pg.K_v] and px > 0:
            Ataque = True
            Izquierda = False 
            Derecha  = False
        # Personaje Quieto
        else:
            Izquierda = False
            Derecha = False
            cuentaPasos = 0
        # Tecla W-Salto
        if not (salto):
            if keys[pg.K_SPACE]:
                salto = True
                Izquierda = False
                Derecha = False
                cuentaPasos = 0
        else:
            if cuentaSalto >= -10:
                py -= (cuentaSalto * abs(cuentaSalto)) * 0.5
                cuentaSalto -= 1
            else:
                cuentaSalto = 10
                salto = False

        # Movimiento de los objetos de colisión
        for objeto in objetos_colision:
            objeto.mover()

        # Detectar colisión con Spider
        rect_personaje = pg.Rect(px, py, ancho, alto)
        rect_spider = pg.Rect(spider.x, spider.y, spider.ancho, spider.alto)
        if detectar_colision(rect_personaje, rect_spider):
            vida_actual -= 1  # Reducir vida en 1
        
        # Detectar colisión de objetos con Spider
        for objeto in objetos_colision:
            rect_objeto = pg.Rect(objeto.x, objeto.y, objeto.ancho, objeto.alto)
            if detectar_colision(rect_objeto, rect_spider):
                vida_actual_spider -= 1  # Reducir vida de Spider en 1
                objetos_colision.remove(objeto)  # Eliminar objeto tras colisión

        recargarPantalla(x,fondo)

    # Salida del Juego
    pg.quit()

   
   

   
main()
