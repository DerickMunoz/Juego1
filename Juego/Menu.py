import pygame as pg
# Inicializar Pygame
pg.init()

# Crear la ventana de Pygame
ancho, alto = 1000, 600
Menu = pg.display.set_mode((ancho, alto))
pg.display.set_caption("Menú del Juego")

# Cargar la imagen de fondo
fondo = pg.image.load("Imagenes/FondoMenu.png").convert()

# Cargar la imagen del botón Inicio
imagen_boton = pg.image.load("Imagenes\\boton inicio.png").convert_alpha()
boton_rect = imagen_boton.get_rect()


# Cargar la imagen del botón Niveles
imagen_niveles = pg.image.load("Imagenes\\boton_Niveles.png").convert_alpha()
boton_rect = imagen_boton.get_rect()

# Cargar la imagen del botón Inicio
imagen_salir = pg.image.load("Imagenes\\Boton_Salir.png").convert_alpha()
boton_rect = imagen_boton.get_rect()


# Calcular las coordenadas centradas para el botón de inicio
x_inicio = (ancho - boton_rect.width) // 2
y_inicio = (alto - boton_rect.height) // 2

# Calcular las coordenadas para el botón de niveles a la izquierda del botón de inicio
x_niveles = x_inicio - boton_rect.width - 120  # 10 píxeles de espacio entre los botones
y_niveles = y_inicio

# Calcular las coordenadas para el botón de salir a la derecha del botón de inicio
x_salir = x_inicio + boton_rect.width + 120  # 10 píxeles de espacio entre los botones
y_salir = y_inicio

# Actualizar las posiciones de los rectángulos
boton_rect.topleft = (x_inicio, y_inicio)
niveles_rect = imagen_niveles.get_rect(topleft=(x_niveles, y_niveles))
salir_rect = imagen_salir.get_rect(topleft=(x_salir, y_salir))

def mostrar_menu_niveles():
    niveles = ["Nivel 1", "Nivel 2", "Nivel 3"]
    fuente = pg.font.Font(None, 36)
    corriendo = True

    while corriendo:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                exit()
            elif evento.type == pg.MOUSEBUTTONDOWN:
                for i, nivel in enumerate(niveles):
                    nivel_rect = pg.Rect(100, 100 + i * 50, 200, 40)
                    if nivel_rect.collidepoint(evento.pos):
                        print(f"{nivel} seleccionado")
                        corriendo = False
                        break
                volver_rect = pg.Rect(100, 100 + len(niveles) * 50, 200, 40)
                if volver_rect.collidepoint(evento.pos):
                    corriendo = False

        Menu.fill((0, 0, 0))
        for i, nivel in enumerate(niveles):
            nivel_texto = fuente.render(nivel, True, (255, 255, 255))
            Menu.blit(nivel_texto, (100, 100 + i * 50))
        volver_texto = fuente.render("Volver", True, (255, 255, 255))
        Menu.blit(volver_texto, (100, 100 + len(niveles) * 50))

        pg.display.flip()

# Bucle principal del menú
corriendo = True
while corriendo:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            corriendo = False
        elif evento.type == pg.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(evento.pos):
                print("Botón de inicio oprimido")
            elif niveles_rect.collidepoint(evento.pos):
                print("Botón de niveles oprimido")
                mostrar_menu_niveles()
            elif salir_rect.collidepoint(evento.pos):
                print("Botón de salir oprimido")
                corriendo = False
    
    if not corriendo:
        break

    # Dibujar el fondo en la ventana del menú
    Menu.blit(fondo, (0, 0))

    # Dibujar las imágenes de los botones
    Menu.blit(imagen_boton, boton_rect.topleft)
    Menu.blit(imagen_niveles, niveles_rect.topleft)
    Menu.blit(imagen_salir, salir_rect.topleft)

    # Actualizar la pantalla
    pg.display.flip()

# Salir de Pygame
pg.quit()