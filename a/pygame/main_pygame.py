import pygame
import random
import sys
import os
import time
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))     # /a/pygame
RUTA_PROYECTO = os.path.dirname(RUTA_ACTUAL)                 # /a

if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from csv_datos import cargar_niveles
from estado_global import crear_estado_global
from partida_pygame import ejecutar_partida_pygame 
from ui_dibujado import dibujar_vertical_degradado, dibujar_texto_centrado
from nucleo_juego import buscar_partida_aleatoria_sin_repetir

niveles = cargar_niveles()
nivel = niveles[0]

datos_partida = buscar_partida_aleatoria_sin_repetir(nivel)  
pygame.init()

PANTALLA = pygame.display.set_mode((900, 600))
FUENTE_PEQUENA = pygame.font.SysFont("arial", 24)
FUENTE_TIMER = pygame.font.SysFont("arial", 32)
CLOCK = pygame.time.Clock()

estado_global = crear_estado_global(tiempo_por_nivel=180)

resultado, puntaje_total = ejecutar_partida_pygame(
    PANTALLA,
    datos_partida, 
    estado_global,
    FUENTE_PEQUENA,
    FUENTE_TIMER,
    CLOCK
)

if resultado == "FIN_TIEMPO":
    mostrar_resumen_final(   
        PANTALLA,
        FUENTE_PEQUENA,
        puntaje_total,
        estado_global["errores_totales"]
    )
def mostrar_resumen_final(pantalla, fuente_pequena, puntos, errores):
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                return
 
        dibujar_vertical_degradado(pantalla, (5, 20, 50), (0, 100, 180))
        dibujar_texto_centrado(pantalla, f"Puntaje total: {puntos}", fuente_pequena, (255,255,255), 180)
        dibujar_texto_centrado(pantalla, f"Errores totales: {errores}", fuente_pequena, (255,200,200), 240)
        dibujar_texto_centrado(pantalla, "Tiempo agotado", fuente_pequena, (200,200,200), 300)

        pygame.display.update()

mostrar_resumen_final(
    PANTALLA,
    FUENTE_PEQ,
    puntaje_total,
    estado_global["errores_totales"]
)