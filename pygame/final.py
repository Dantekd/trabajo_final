#Fijarte de donde salen los puntos por cada palabra descubierta
import pygame
import random
import sys
import os

# Rutas que conectan con los archivo fuera de la carpeta pygame
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))     
RUTA_PROYECTO = os.path.dirname(RUTA_ACTUAL)                 

if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

#Imports que se utilizan
from csv_datos import cargar_niveles
from nucleo_juego import preparar_partida, buscar_partida_aleatoria_sin_repetir
from nucleo_pygame import crear_estado_pygame,inicializar_partida_pygame
from logicas_pygame import *
from ui_dibujado import *
from ui_botones import *
from audio_pygame import controlar_audio
from acciones_jugador import *
from login_pygame import pantalla_login,  pantalla_configuracion,cargar_datos_json,guardar_datos_json

pygame.init()
#Con esto te aparece la pantalla de login 
indice_usuario = pantalla_login()
#Esto seria la siguiente etapa del login donde se selecciona el modo
perfil = pantalla_configuracion(indice_usuario)
#Tamaño de la pantalla
PANTALLA = pygame.display.set_mode((900, 600))
#titulo del juego
pygame.display.set_caption("Descubre la palabra - Encina")
#Musica de fondo 
pygame.mixer.music.load("Final/pygame/sonido/fondo.mp3")
#bucle infinito
pygame.mixer.music.play(-1)

DIMENSION = (900, 600)

#Icono del juego
icono = pygame.image.load("Final/pygame/icono_juego.png")
pygame.display.set_icon(icono)

#El tipo de fuente que se utiliza en el juego
FUENTE_TITULO=pygame.font.SysFont("Old English Text",90)
FUENTE = pygame.font.SysFont(None, 48)
FUENTE_PEQUENA = pygame.font.SysFont(None, 32)
FUENTE_TIMER = pygame.font.SysFont(None, 28)
R_CLOCK = pygame.time.Clock()

#Panel de control de sonido 
sonido_arriba = pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "subir_volumen.png"))
sonido_arriba = pygame.transform.scale(sonido_arriba, (40, 40))
sonido_abajo  = pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "bajar_volumen.png"))
sonido_abajo = pygame.transform.scale(sonido_abajo, (40, 40))
sonido_mute   = pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "mute_volumen.png"))
sonido_mute = pygame.transform.scale(sonido_mute, (40, 40))
sonido_max= pygame.image.load(os.path.join(RUTA_ACTUAL, "sonido", "maximo_volumen.png"))
sonido_max = pygame.transform.scale(sonido_max, (40, 40))


#Aca ya es la parte de la ejecución y poner en practica lo que se desarrollo en las funciones
def ejecutar_partida_pygame(partida):
    #Aca se llama a la función que se hizo arriba 
    datos = inicializar_partida_pygame(partida, perfil,indice_usuario)
    estado = datos["estado"]
    #Para que muestre nivel y partida en el juego 
    estado["nivel_actual"] = partida["nivel_actual"]
    estado["partida_actual"] = partida["partida_actual"]
    #Controla los botones que aun no se usaron
    botones_disponibles = datos["botones_disponibles"]
    botones_usados = datos["botones_usados"]
    botones_accion = datos["botones_accion"]
    #Controla los comodines usados
    comodines_usados = datos["comodines_usados"]
    #Controla el tieempo restantes
    tiempo_restante = datos["tiempo_restante"]
    #Los botones de los comdines 
    botones_comodines = datos["botones_comodines"]
   
    #Datos base que se van a utilizar
    clock = pygame.time.Clock()
    running = True
    cambio_nivel = None
    mensaje_timer = 0
    mensaje = ""
    intencion=""
    #mientras este activo el programa 
    while running:
        #El tiempo va a ser de 
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()
        #Esto te permite salir al tocar X En la ventana
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # eventos de partida
            resultado = manejar_eventos_partida(ev,estado,botones_disponibles,botones_usados,botones_accion,botones_comodines,comodines_usados)

            if resultado is not None:
                tipo, valor = resultado
                #Comodines
                if tipo == "revelar":
                    estado["mensaje_comodin"] = f"Palabra: {valor}"
                    estado["mensaje_comodin_timer"] = 7

                elif tipo == "ubicar":
                    estado["mensaje_comodin"] = f"La letra '{valor.upper()}' está en todas las palabras"
                    estado["mensaje_comodin_timer"] = 7

                elif tipo == "nivel":
                    estado["mensaje_comodin"] = f"Resultado del comodín: {valor.upper()}"
                    estado["mensaje_comodin_timer"] = 2
                    cambio_nivel = valor
                    running = False
            # tiempo
        tiempo_restante = actualizar_tiempo(tiempo_restante, dt)

            # Lo que te aparece en el fin de juego
        fin, intencion_tiempo = verificar_fin_juego(estado, tiempo_restante)

        if intencion_tiempo and intencion_tiempo != estado["ultimo_mensaje"]:
            estado["mensaje_comodin"] = intencion_tiempo
            estado["mensaje_comodin_timer"] = 2
            estado["ultimo_mensaje"] = intencion_tiempo

        if fin:
            intencion = intencion_tiempo
            running = False
        #Lo que ve el usuario
        dibujar_juego(PANTALLA,estado,botones_disponibles,botones_usados,FUENTE_PEQUENA,FUENTE_TIMER,tiempo_restante,mensaje,mensaje_timer,dt)
        dibujar_botones_accion(PANTALLA, botones_accion, FUENTE_PEQUENA)
        dibujar_comodines(PANTALLA, botones_comodines, comodines_usados, FUENTE_PEQUENA)
        controlar_audio(keys, PANTALLA, sonido_arriba, sonido_abajo, sonido_mute, sonido_max)

        pygame.display.update()

    return estado["puntaje"], estado["errores"],intencion, cambio_nivel


# Maneja el flujo de niveles y partidas
def jugar_toda_la_partida(max_niveles: int = 5, max_partidas_por_nivel: int = 3):
    #Datos base que se van a usar
    niveles = cargar_niveles()
    puntaje_total = 0
    intentos_restantes = 3
    i_nivel = 0
    errores_total= 0
    datos = cargar_datos_json()                 
    usuario = datos["usuarios"][indice_usuario]  
    # limitar a lo disponible y a max_niveles
    limite_niveles = len(niveles)
    #Lo pone limite a la pogresion de niveles
    if limite_niveles > max_niveles:
        limite_niveles = max_niveles    
    #nivel actual < limite de nivel
    while i_nivel < limite_niveles:
        nivel = niveles[i_nivel]
        partidas_jugadas = 0
        # jugar hasta max_partidas_por_nivel o hasta agotar partidas
        while partidas_jugadas < max_partidas_por_nivel and partidas_jugadas < len(nivel["partidas"]):
            # obtener partida aleatoria sin repetir, los comodines se resetean al pasar de nivel
            
            datos = buscar_partida_aleatoria_sin_repetir(nivel)
            datos["nivel_actual"] = i_nivel + 1
            datos["partida_actual"] = partidas_jugadas + 1
            puntos,errores,intencion,cambio_nivel = ejecutar_partida_pygame(datos)
            if intencion == "tiempo":
                intentos_restantes -= 1
                if intentos_restantes == 0:
                    mostrar_resumen_final(puntaje_total, errores_total)
                    return #Sale de todo los bucles
                else:
                    partidas_jugadas = 0
                    continue
            if intencion == "victoria":
                pass 
            # mostrar pantalla de resumen y esperar tecla para continuar
            if usuario["accesibilidad"]["tdah"]:
                mostrar_resumen_partida(puntos, errores)
            #Este es el acumulador de puntaje 
            puntaje_total += puntos
            #Este es el acumulador de errores
            errores_total += errores
            #Trae los datos existentes en Json y los usa
            datos = cargar_datos_json()
            usuario = datos["usuarios"][indice_usuario]

            usuario["stats"]["puntaje_total"] += puntaje_total
            usuario["stats"]["errores_totales"] += errores_total
            usuario["stats"]["partidas_jugadas"] += 1
            #Los guarda en el Json
            guardar_datos_json(datos)
            #Parte apicable del 50/50
            #Hace que cambie de nivel hacia uno mas arriba
            if cambio_nivel == "subir":
                i_nivel += 1
                break
            #Hace que cambie de nivel hacia uno más abajo
            elif cambio_nivel == "bajar":
                if i_nivel > 0:
                    i_nivel -= 1
                    break
                else:
                    partidas_jugadas = 0   
                    continue
            #Y si esta en el nivel 1 y pierde el 50/50 resetea la partida
            elif cambio_nivel == "reset":
                partidas_jugadas = 0       
                continue
            #suma a el contenedor de partidas jugadas para que al llegar a cierta cantidad avanzar de nivel
            partidas_jugadas += 1 
        else:
            i_nivel += 1
    mostrar_resumen_final(puntaje_total, errores_total)



#Resultados de la partida
def mostrar_resumen_partida(puntos_obtenidos: int,errores:int):
    # pinta una pantalla simple con el puntaje de la partida y espera tecla para seguir
    espera = True
    while espera:
        for ev in pygame.event.get():#Averiguar
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                espera = False
        #Este es el fondo diferente al terminar la partida
        dibujar_vertical_degradado(PANTALLA, (0, 0, 80), (0, 150, 255))
        #Dibuja el texto que aparecera en el resumen de la partida
        dibujar_texto_centrado(PANTALLA, f"Puntos de esta partida: {puntos_obtenidos}", FUENTE, (255, 255, 255), 200)
        dibujar_texto_centrado(PANTALLA, f"Errores de esta partida: {errores}", FUENTE, (255, 255, 255), 260)
        dibujar_texto_centrado(PANTALLA, "Presiona cualquier tecla para continuar...", FUENTE_PEQUENA, (200, 200, 200), 340)
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
        #Fondo de resumen final
        dibujar_vertical_degradado(PANTALLA, (5, 20, 50), (0, 100, 180))
        #Texto que aparece al terminar
        dibujar_texto_centrado(PANTALLA, f"GAME OVER", FUENTE_TITULO, (255, 255, 255), 150)
        dibujar_texto_centrado(PANTALLA, f"Puntaje total: {puntaje_total}", FUENTE, (255, 255, 255), 260)
        dibujar_texto_centrado(PANTALLA, f"errores total: {errores_total}", FUENTE, (255, 255, 255), 330)
        dibujar_texto_centrado(PANTALLA, "Juego finalizado. Presiona cualquier tecla para salir.", FUENTE_PEQUENA, (200, 200, 200), 420)
        pygame.display.update()
# max nivel 5 y max partidas 3
if __name__ == "__main__":
    jugar_toda_la_partida(max_niveles=5, max_partidas_por_nivel=3)
    pygame.quit()
