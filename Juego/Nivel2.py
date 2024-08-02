import pygame as pg
import random
import sys

class Niveles:
    @staticmethod
    def Nivel2():
        pg.init()
        w, h = 1000, 600
        fondo = pg.image.load("Imagenes\\Fondo_Nivel2.png").convert()

        PANTALLA = pg.display.set_mode((w, h))
        pg.display.set_caption("Nivel 2")

        ejecuta = True

        while ejecuta:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    ejecuta = False

            PANTALLA.blit(fondo, (0, 0))  # Dibujar el fondo

            pg.display.flip()  # Actualizar la pantalla

        pg.quit()