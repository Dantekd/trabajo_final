import pygame
import sys
import random
import os 
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))     
RUTA_PROYECTO = os.path.dirname(RUTA_ACTUAL)                 

if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from csv_datos import cargar_niveles
from nucleo_juego import preparar_partida, buscar_partida_aleatoria_sin_repetir
from nucleo_pygame import crear_estado_pygame
from ui_dibujado import *
from ui_botones import *
from acciones_jugador import *
from logicas_pygame import *

pygame.init()

PANTALLA = pygame.display.set_mode((900, 600))
pygame.display.set_caption("DEMO CONFIGURABLE")

FUENTE = pygame.font.SysFont(None, 48)
FUENTE_PEQUENA = pygame.font.SysFont(None, 32)
FUENTE_TIMER = pygame.font.SysFont(None, 28)


# Ejecuta una partida de la demo
def pantalla_demo_config():
    niveles = 0
    partidas = 0
    seleccionando = True
    while seleccionando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:

                # Modifica niveles con flechas arriba y abajo
                if ev.key == pygame.K_UP and niveles < 5:
                    niveles += 1
                if ev.key == pygame.K_DOWN and niveles > 1:
                    niveles -= 1

                # Modifica partidas con flechas derecha e izquierda
                if ev.key == pygame.K_RIGHT and partidas < 7:
                    partidas += 1
                if ev.key == pygame.K_LEFT and partidas > 1:
                    partidas -= 1

                if ev.key == pygame.K_RETURN:
                    seleccionando = False

        PANTALLA.fill((30, 30, 30))

        dibujar_texto_centrado(PANTALLA, "DEMO CONFIGURABLE", FUENTE, (255,255,255), 100)
        dibujar_texto_centrado(PANTALLA, f"Niveles: ({niveles})", FUENTE_PEQUENA, (255,255,0), 250)
        dibujar_texto_centrado(PANTALLA, f"Partidas por nivel: ({partidas})", FUENTE_PEQUENA, (255,255,0), 300)
        dibujar_texto_centrado(PANTALLA, "Usa flechas para modificar", FUENTE_PEQUENA, (180,180,180), 350)

        pygame.display.update()

    return niveles, partidas



# Ejecuta las partidas de la demo 
def ejecutar_partida_demo(partida, nivel_actual, partida_actual):

    base_set, base_lista, palabras_validas = preparar_partida(partida)
    # Guarda nivel y número de partida actual
    estado = crear_estado_pygame(base_lista, palabras_validas, "normal")
    estado["tdah"] = True
    estado["nivel_actual"] = nivel_actual
    estado["partida_actual"] = partida_actual
    # Mezcla letras
    letras = base_lista[:]
    random.shuffle(letras)
    # Crea todos lso botones
    botones_disponibles = crear_botones_letras_csv(letras)
    botones_usados = []
    botones_accion = crear_botones_accion()
    mensaje_timer = 0
    mensaje = ""
    tiempo_restante = 60
    clock = pygame.time.Clock()

    corriendo = True
    while corriendo:

        dt = clock.tick(60) / 1000

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                manejar_click_botones(pos, botones_disponibles, botones_usados, estado["palabra_actual"])
                manejar_click_usados(pos, botones_disponibles, botones_usados, estado["palabra_actual"])

                for b in botones_accion:
                    if b["rect"].collidepoint(pos):
                        manejar_accion_jugador(b["accion"], estado, botones_usados, botones_disponibles)

            if ev.type == pygame.KEYDOWN:
                accion = detectar_accion_teclado(ev)
                if accion:
                    manejar_accion_jugador(accion, estado, botones_usados, botones_disponibles)
        # Actualiza tiempo
        tiempo_restante = actualizar_tiempo(tiempo_restante, dt)
        # Verifica fin de partida
        fin, motivo = verificar_fin_juego(estado, tiempo_restante)
        if fin:
            corriendo = False

        # Dibuja todo el juego
        dibujar_juego( PANTALLA,estado,botones_disponibles,botones_usados,FUENTE_PEQUENA,FUENTE_TIMER,tiempo_restante,mensaje,mensaje_timer,dt)

        # Muestra las palabras que tenes que escribir en cada nivel
        dibujar_palabras_objetivo(PANTALLA, estado["palabras_validas"], FUENTE_PEQUENA)

        pygame.display.update()


# Ejecuta la demo completa
def jugar_demo():
    niveles_max, partidas_max = pantalla_demo_config()
    niveles = cargar_niveles()
    i_nivel = 0
    # Recorre niveles sin pasarse del máximo elegido
    while i_nivel < niveles_max and i_nivel < len(niveles):
        nivel = niveles[i_nivel]
        i_partida = 0
        # Recorre partidas sin pasarse del máximo elegido
        while i_partida < partidas_max and i_partida < len(nivel["partidas"]):
            partida = buscar_partida_aleatoria_sin_repetir(nivel)
            ejecutar_partida_demo(partida,i_nivel + 1,i_partida + 1)

            i_partida += 1
        i_nivel += 1

if __name__ == "__main__":
    jugar_demo()
    pygame.quit()