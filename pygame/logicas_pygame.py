import pygame
import random
from pygame.locals import *


def actualizar_tiempo(tiempo_restante, dt):

    nuevo_tiempo = tiempo_restante - dt

    return nuevo_tiempo

def obtener_evento_tecla():
    """Devuelve una letra presionada o '__SALIR__' o None."""
    salida = None  # Valor por defecto
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == QUIT:
            salida = "__SALIR__"
            break
        else:
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    salida = "__SALIR__"
                    break
                else:
                    tecla = evento.unicode
                    if tecla.isalpha():
                        salida = tecla.upper()
                        break
    return salida  

def verificar_fin_juego(estado, tiempo_restante):

    fin = False
    mensaje = ""

    if tiempo_restante <= 0:
        fin = True
        mensaje = "Se acabó el tiempo"

    if estado.get("errores", 0) >= estado.get("intentos_maximos", 5):
        fin = True
        mensaje = "Máximos errores alcanzados"

    if len(estado["palabras_encontradas"]) >= len(estado["palabras_validas"]):
        fin = True
        mensaje = "No quedan palabras"

    return fin, mensaje


def manejar_click_comodines(pos, botones, comodines_nivel, estado, tiempo_restante,botones_disponibles):

    cambio_nivel = None
    
    for b in botones:
        if b["rect"].collidepoint(pos):

            nombre = b["tipo"]
            #Suma 30 segudno al tiempo
            if nombre == "tiempo" and not comodines_nivel["tiempo"]:
                tiempo_restante += 30
                comodines_nivel["tiempo"] = True
            #Resea los errores de la partida mientras que aun no hayas llegado a los 5 errores
            elif nombre == "errores" and not comodines_nivel["errores"]:
                estado["errores"] = 0
                comodines_nivel["errores"] = True
                b["activa"] = False
            #sirve para definir si sube o baja de nivel cuando usa el comodin
            elif nombre == "nivel" and not comodines_nivel["nivel"]:

                comodines_nivel["nivel"] = True

                cambio_nivel = "usar_comodin"

    return tiempo_restante, cambio_nivel

#Es la funcion complementaria de el comodin 50/50
def usar_comodin_nivel(nivel_actual, nivel_minimo):

    cambio = ""

    numero = random.randint(0, 1)

    if numero == 1:
        cambio = "subir"

    else:
        if nivel_actual > nivel_minimo:
            cambio = "bajar"
        else:
            cambio = "reset"

    return cambio