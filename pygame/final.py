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
from acciones_jugador import *
from login_pygame import pantalla_login,  pantalla_configuracion

# ========== INICIALIZACION PYGAME ==========
pygame.init()
#El juego incorpora música de fondo controlada mediante eventos de teclado. El sistema de audio está desacoplado
#de la lógica del juego y permite subir, bajar, mutear o maximizar el volumen. Para perfiles con adaptación 
#TEA, el volumen inicial se reduce y no se reproducen sonidos abruptos, manteniendo la funcionalidad completa.
indice_usuario = pantalla_login()
#El perfil se obtiene a partir del sistema de login y configuración, donde cada usuario selecciona una 
# configuración que luego se utiliza para adaptar aspectos del juego como el volumen y la interfaz.
perfil = pantalla_configuracion(indice_usuario)
pygame.mixer.music.load("Final/pygame/sonido/fondo.mp3")
pygame.mixer.music.play(-1)
if perfil == "tea":
    pygame.mixer.music.set_volume(0.02)
else:
    pygame.mixer.music.set_volume(0.05)

DIM = (900, 600)#averiguar que es D
PANTALLA = pygame.display.set_mode((900, 600))
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


def inicializar_partida_pygame(partida, perfil):
    base_set, base_lista, palabras_validas = preparar_partida(partida)

    estado = crear_estado_pygame(base_lista, palabras_validas, perfil)
    #Randomizador de botones_letras_csv
    letras = base_lista[:]
    random.shuffle(letras)

    datos_partida = {
        "estado": estado,
        "botones_disponibles": crear_botones_letras_csv(letras),
        "botones_usados": [],
        "botones_accion": crear_botones_accion(),
        "botones_comodines": crear_botones_comodines(),
        "comodines_usados": {"revelar": False, "ubicar": False, "nivel": False},
        "tiempo_restante": 60
    }

    return datos_partida


def ejecutar_partida_pygame(partida):

    datos = inicializar_partida_pygame(partida, perfil)

    estado = datos["estado"]
    #Controla los botones que aun no se usaron
    botones_disponibles = datos["botones_disponibles"]
    botones_usados = datos["botones_usados"]
    botones_accion = datos["botones_accion"]
    comodines_usados = datos["comodines_usados"]
    tiempo_restante = datos["tiempo_restante"]
    #Los botones de los comdines 
    botones_comodines = datos["botones_comodines"]
   
    #Tiempo
    clock = pygame.time.Clock()
    running = True
    cambio_nivel = None
    mensaje = ""
    mensaje_timer = 0
    

    while running:
        
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # eventos de partida
            resultado = manejar_eventos_partida(ev,estado,botones_disponibles,botones_usados,botones_accion,botones_comodines,comodines_usados)

            if resultado is not None:
                tipo, valor = resultado

                if tipo == "revelar":
                    estado["mensaje"] = f"Palabra: {valor}"
                    estado["mensaje_timer"] = 3

                elif tipo == "ubicar":
                    estado["mensaje"] = f"La letra '{valor.upper()}' está en todas las palabras"
                    estado["mensaje_timer"] = 3

                elif tipo == "nivel":
                    estado["mensaje"] = f"Resultado del comodín: {valor.upper()}"
                    estado["mensaje_timer"] = 2
                    cambio_nivel = valor
                    running = False
            # tiempo
        tiempo_restante = actualizar_tiempo(tiempo_restante, dt)

            # Lo que te aparece en el fin de juego
        fin, msg = verificar_fin_juego(estado, tiempo_restante)
        if fin:
            mensaje = msg
            running = False

            #
        mensaje_timer = dibujar_juego(PANTALLA,estado,botones_disponibles,botones_usados,FUENTE_PEQUENA,FUENTE_TIMER,tiempo_restante,mensaje,mensaje_timer,dt)
        dibujar_botones_accion(PANTALLA, botones_accion, FUENTE_PEQUENA)
        dibujar_comodines(PANTALLA, botones_comodines, comodines_usados, FUENTE_PEQUENA)
        controlar_audio(keys, PANTALLA, sonido_arriba, sonido_abajo, sonido_mute, sonido_max)

        pygame.display.update()

    return estado["puntaje"], estado["errores"], False, cambio_nivel


def manejar_eventos_partida(ev, estado, botones_disponibles, botones_usados,botones_accion, botones_comodines, comodines_usados):

    cambio_nivel = None
    
    # ===== DETECCION DE EVENTOS =====
    if ev.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()

        manejar_click_botones(pos, botones_disponibles, botones_usados, estado["palabra_actual"])
        manejar_click_usados(pos, botones_disponibles, botones_usados, estado["palabra_actual"])

        for b in botones_accion:
            if b["rect"].collidepoint(pos):
                manejar_accion_jugador(b["accion"], estado, botones_usados,  botones_disponibles)
        
        # solo detecta comodín
        resultado = manejar_click_comodines(pos, botones_comodines, comodines_usados, estado)

        if resultado is not None:
            cambio_nivel = resultado
    elif ev.type == pygame.KEYDOWN:
        accion = detectar_accion_teclado(ev)

        if accion is not None:
            manejar_accion_jugador(accion,estado,botones_usados,botones_disponibles)

    return cambio_nivel

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
        # jugar hasta max_partidas_por_nivel o hasta agotar partidas
        while partidas_jugadas < max_partidas_por_nivel and partidas_jugadas < len(nivel["partidas"]):
            # obtener partida aleatoria sin repetir, los comodines se resetean al pasar de nivel
            
            datos = buscar_partida_aleatoria_sin_repetir(nivel)
            puntos,errores,game_over,cambio_nivel = ejecutar_partida_pygame(datos)
            
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
        R_CLOCK.tick(30)
        pygame.display.update()
        

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
        R_CLOCK.tick(30)
        pygame.display.update()
# max nivel 5 y max partidas 3
if __name__ == "__main__":
    jugar_toda_la_partida(max_niveles=5, max_partidas_por_nivel=1)
    pygame.quit()
