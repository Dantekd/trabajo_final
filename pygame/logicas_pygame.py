
import random
from pygame.locals import *
from comodines import comodin_revelar_palabra,comodin_ubicar_letra,comodin_nivel


#Actualiza el tiempo en cada partida
def actualizar_tiempo(tiempo_restante, dt):

    nuevo_tiempo = tiempo_restante - dt

    return nuevo_tiempo


#Esto le pone condiciones para que el juego termine mostrandote la pantalla de fin y un mensaje

def verificar_fin_juego(estado, tiempo_restante):

    fin = False
    mensaje = ""
    
    if tiempo_restante <= 0:
        fin = True
        mensaje = "Se acabó el tiempo"


    if len(estado["palabras_encontradas"]) >= len(estado["palabras_validas"]):
        fin = True
        mensaje = "No quedan palabras"

    return fin, mensaje



def obtener_comodin_cambiar_partida(datos_partida):
    """Extrae el comodín desde el nivel de la partida, con validación."""
    
    resultado = False

    nivel = datos_partida.get("nivel")
    if nivel != None:
        valor = nivel.get("comodin_cambiar_partida")
        if valor != None:
            resultado = valor

    return resultado
   

def manejar_click_comodines(pos, botones_comodines, comodines_usados, estado):
    """
    Maneja el click sobre los botones de comodines.
    Devuelve una tupla (tipo, valor) o None.
    """
    
    resultado = None

    for b in botones_comodines:
        if b["rect"].collidepoint(pos):

            tipo = b["tipo"]

            if comodines_usados[tipo]:
                break

            if tipo == "revelar":
                palabra = comodin_revelar_palabra(estado)
                comodines_usados[tipo] = True
                resultado = ("revelar", palabra)

            elif tipo == "ubicar":
                letra = comodin_ubicar_letra(estado)
                comodines_usados[tipo] = True
                resultado = ("ubicar", letra)

            elif tipo == "nivel":
                accion = comodin_nivel()
                comodines_usados[tipo] = True
                resultado = ("nivel", accion)

            break

    return resultado
