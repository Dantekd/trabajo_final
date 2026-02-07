#Fijarte de donde salen los puntos por cada palabra descubierta
import pygame
import random
import sys
import os

# ========== RUTAS ==========
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))     
RUTA_PROYECTO = os.path.dirname(RUTA_ACTUAL)                 

if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

# ========== IMPORTS DEL PROYECTO ==========
from csv_datos import cargar_niveles
from nucleo_juego import preparar_partida, buscar_partida_aleatoria_sin_repetir
from nucleo_pygame import crear_estado_pygame,procesar_palabra_pygame
from logicas_pygame import *
from ui_dibujado import *
from ui_botones import *
from audio_pygame import controlar_audio

# ========== INICIALIZACION PYGAME ==========
pygame.init()
#Musica de fondo
pygame.mixer.music.load("Final/pygame/sonido/fondo.mp3")
pygame.mixer.music.play(-1)

DIM = (900, 600)#averiguar que es D
PANTALLA = pygame.display.set_mode(DIM)
#titulo del juego
pygame.display.set_caption("AHORCADO - Encina")
#Icono del juego
icono = pygame.image.load("Final/pygame/icono_juego.png")
pygame.display.set_icon(icono)

#El tipo de fuente que se utiliza en el juego
FUENTE = pygame.font.SysFont(None, 48)
FUENTE_PEQUENA = pygame.font.SysFont(None, 32)
FUENTE_TIMER = pygame.font.SysFont(None, 28)
R_CLOCK = pygame.time.Clock()

#Sonido 
sonido_arriba = pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "subir_volumen.png"))
sonido_arriba = pygame.transform.scale(sonido_arriba, (40, 40))
sonido_abajo  = pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "bajar_volumen.png"))
sonido_abajo = pygame.transform.scale(sonido_abajo, (40, 40))
sonido_mute   = pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "mute_volumen.png"))
sonido_mute = pygame.transform.scale(sonido_mute, (40, 40))
sonido_max= pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "maximo_volumen.png"))
sonido_max = pygame.transform.scale(sonido_max, (40, 40))


# ========== LOGICA DE PARTIDA (HÍBRIDA) ==========

def ejecutar_partida_pygame(partida: dict,comodines_nivel: dict):

    base_set, base_lista, palabras_validas = preparar_partida(partida)

    estado = crear_estado_pygame(base_lista, palabras_validas)

    botones_usados = []
    palabra_actual = []

    #Randomizador de botones_letras_csv
    letras_mezcladas = base_lista[:]
    random.shuffle(letras_mezcladas)
    #Controla los botones que aun no se usaron
    botones_disponibles = crear_botones_letras_csv(letras_mezcladas)
    #Los botones de los comdines 
    botones_comodines = crear_botones_comodines()
    #Tiempo
    tiempo_restante = 60
    #
    
    

    clock = pygame.time.Clock()

    mensaje = ""
    mensaje_timer = 0

    running = True
    fin_partida = False
    fin_juego = False
    cambio_nivel = None
    while running:

        keys = pygame.key.get_pressed()
        dt = clock.tick(60) / 1000

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()

                manejar_click_botones(pos, botones_disponibles, botones_usados, palabra_actual)
                manejar_click_usados(pos, botones_disponibles, botones_usados, palabra_actual)

                #es lo que trae el funcionamiento al hacer click en el comodin
                tiempo_restante, cambio= manejar_click_comodines(pos,botones_comodines,comodines_nivel,estado,tiempo_restante,botones_disponibles)
                #Para que no se pise con el cambio de nivel
                if cambio is not None:
                    cambio_nivel = cambio
                    running=False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:

                    if len(palabra_actual) > 0:

                        palabra = "".join(palabra_actual)

                        resultado = procesar_palabra_pygame(estado, palabra)

                        if resultado == "valida":
                            mensaje = "Palabra válida"
                        elif resultado == "repetida":
                            mensaje = "Palabra repetida"
                        else:
                            mensaje = "Palabra inválida"

                        palabra_actual.clear()
                        botones_usados.clear()

                        for b in botones_disponibles:
                            b["activa"] = True
        tiempo_restante = actualizar_tiempo(tiempo_restante, dt)

        fin, msg = verificar_fin_juego(estado, tiempo_restante)

        if fin:
            running = False
            mensaje = msg
        # SOLO si perdió del todo
        if estado["errores"] >= 5:
            fin_juego = True

        mensaje_timer = dibujar_juego(PANTALLA,estado,botones_disponibles,botones_usados,FUENTE_PEQUENA,FUENTE_TIMER,tiempo_restante,mensaje,mensaje_timer,dt)

        dibujar_comodines(PANTALLA, botones_comodines, comodines_nivel, FUENTE_PEQUENA)

        controlar_audio(keys, PANTALLA, sonido_arriba, sonido_abajo, sonido_mute, sonido_max)

        pygame.display.update()

    return estado["puntaje"], estado["errores"], fin_juego, cambio_nivel


# ========== FLUJO DE NIVELES Y PARTIDAS ==========
def jugar_toda_la_partida(max_niveles: int = 5, max_partidas_por_nivel: int = 3):
    niveles = cargar_niveles()
    puntaje_total = 0
    i_nivel = 0
    errores_total= 0
    # limitar a lo disponible y a max_niveles
    limite_niveles = len(niveles)
    #Lo pone limite a la pogresion de niveles
    if limite_niveles > max_niveles:
        limite_niveles = max_niveles


    while i_nivel < limite_niveles:
        
        nivel = niveles[i_nivel]
        partidas_jugadas = 0
        comodines_nivel = {
                "tiempo": False,
                "errores": False,
                "nivel": False
            }
        # jugar hasta max_partidas_por_nivel o hasta agotar partidas
        while partidas_jugadas < max_partidas_por_nivel and partidas_jugadas < len(nivel["partidas"]):
            # obtener partida aleatoria sin repetir
            # 👇 COMODINES SE RESETEAN SOLO AL CAMBIAR NIVEL
            
            datos = buscar_partida_aleatoria_sin_repetir(nivel)
            puntos,errores,game_over,cambio_nivel = ejecutar_partida_pygame(datos,comodines_nivel)
            
            if cambio_nivel == "usar_comodin":
                cambio_nivel = usar_comodin_nivel(i_nivel, 0)
            # mostrar pantalla de resumen y esperar tecla para continuar
            mostrar_resumen_partida(puntos,errores)
            puntaje_total += puntos
            errores_total += errores
            # FIN JUEGO: mostrar puntaje y errores totalales
            if game_over:
                mostrar_resumen_final(puntaje_total,errores_total)
                return
           
            if cambio_nivel == "subir":
                i_nivel += 1
                break

            elif cambio_nivel == "bajar":
                if i_nivel > 0:
                    i_nivel -= 1
                    break
                else:
                    partidas_jugadas = 0   
                    continue

            elif cambio_nivel == "reset":
                partidas_jugadas = 0       
                continue
            #suma a el contenedor de partidas jugadas para que al llegar a cierta cantidad avanzar de nivel
            partidas_jugadas += 1 
        else:
            i_nivel += 1



#Resultados de la partida
def mostrar_resumen_partida(puntos_obtenidos: int,errores:int):
    # pinta una pantalla simple con el puntaje de la partida y espera tecla para seguir
    espera = True
    while espera:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                espera = False

        dibujar_vertical_degradado(PANTALLA, (0, 0, 80), (0, 150, 255))
        dibujar_texto_centrado(PANTALLA, f"Puntos de esta partida: {puntos_obtenidos}", FUENTE, (255, 255, 255), 200)
        dibujar_texto_centrado(PANTALLA, f"Errores de esta partida: {errores}", FUENTE, (255, 255, 255), 260)
        dibujar_texto_centrado(PANTALLA, "Presiona cualquier tecla para continuar...", FUENTE_PEQUENA, (200, 200, 200), 340)
        pygame.display.update()
        R_CLOCK.tick(30)

#Te muestro lo que datos y diseño que hay al finalizar el juego
def mostrar_resumen_final(puntaje_total, errores_total):
    espera = True
    while espera:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                espera = False 

        dibujar_vertical_degradado(PANTALLA, (5, 20, 50), (0, 100, 180))
        dibujar_texto_centrado(PANTALLA, f"Puntaje total: {puntaje_total}", FUENTE, (255, 255, 255), 200)
        dibujar_texto_centrado(PANTALLA, f"errores total: {errores_total}", FUENTE, (255, 255, 255), 260)
        dibujar_texto_centrado(PANTALLA, "Juego finalizado. Presiona cualquier tecla para salir.", FUENTE_PEQUENA, (200, 200, 200), 320)
        pygame.display.update()
        R_CLOCK.tick(30)

# max nivel 5 y max partidas 3
# ========== START ==========
if __name__ == "__main__":
    jugar_toda_la_partida(max_niveles=5, max_partidas_por_nivel=1)
    pygame.quit()
