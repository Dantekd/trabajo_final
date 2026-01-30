
import sys
import os

# Ruta de este archivo
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))

# Ruta de la carpeta donde están tus módulos (carpeta "a")
RUTA_MODULOS = os.path.dirname(RUTA_ACTUAL)  

if RUTA_MODULOS not in sys.path:
    sys.path.append(RUTA_MODULOS)

from csv_datos import cargar_niveles
from nucleo_juego import preparar_partida, buscar_partida_aleatoria_sin_repetir
from mecanicas import generar_guiones
from logicas_pygame import dibujar_vertical_degradado
import random
import pygame


pygame.init()

DIMENSIONES_PANTALLA = (800, 500)
PANTALLA = pygame.display.set_mode(DIMENSIONES_PANTALLA)
pygame.display.set_caption("AHORCADO Encina-Diaz")

icono = pygame.image.load(r"C:\Users\Usuario\Desktop\Segundo_parcial\a\pygame\icono_juego.jpg")
pygame.display.set_icon(icono)

# CARGA DE DATOS
niveles = cargar_niveles()
nivel_actual = niveles[0]  # nivel 1
partida = random.choice(nivel_actual["partidas"])

base_set, base_lista, palabras_validas = preparar_partida(partida)
guiones = generar_guiones(partida["base"])

palabra_actual = ""

# CREAR BOTONES DE LETRAS
def crear_botones(letras):
    botones = []
    x = 50
    for letra in letras:
        rect = pygame.Rect(x, 400, 40, 40)
        botones.append((letra, rect))
        x += 50
    return botones

botones = crear_botones(base_lista)

clock = pygame.time.Clock()
TIEMPO_LIMITE = 10000  # 10 segundos
inicio = pygame.time.get_ticks()

funciona = True

while funciona:
    # EVENTOS
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            funciona = False

        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for letra, rect in botones:
                if rect.collidepoint(pos):
                    palabra_actual += letra.upper()

    # TIMER
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - inicio >= TIEMPO_LIMITE:
        funciona = False

    # LIMPIAR PANTALLA CON DEGRADADO
    dibujar_vertical_degradado(PANTALLA, (0, 0, 80), (0, 150, 255))

    # DIBUJAR TEXTO
    font = pygame.font.SysFont(None, 48)

    txt = font.render(guiones, True, (255, 255, 255))
    PANTALLA.blit(txt, (200, 100))

    txt2 = font.render(palabra_actual, True, (255, 255, 0))
    PANTALLA.blit(txt2, (200, 200))

    # DIBUJAR BOTONES
    for letra, rect in botones:
        pygame.draw.rect(PANTALLA, (100, 100, 255), rect)
        t = font.render(letra.upper(), True, (0, 0, 0))
        PANTALLA.blit(t, (rect.x + 10, rect.y + 5))

    pygame.display.flip()
    clock.tick(60)  # FPS NORMAL

pygame.quit()