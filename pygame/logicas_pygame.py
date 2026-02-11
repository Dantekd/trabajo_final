
import pygame
from pygame.locals import *
from comodines import comodin_revelar_palabra,comodin_ubicar_letra,comodin_nivel
from acciones_jugador import *

#Actualiza el tiempo en cada partida
def actualizar_tiempo(tiempo_restante, dt):
    #dt es el tiempo que paso desde ultimo frame 
    nuevo_tiempo = tiempo_restante - dt

    return nuevo_tiempo

#Son todas las acciones que puede hacer el jugador durante la partida
def manejar_eventos_partida(ev, estado, botones_disponibles, botones_usados,botones_accion, botones_comodines, comodines_usados):

    cambio_nivel = None
    
    #Detecta los eventos cuando haces click
    if ev.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        #Esto seria los botones que aun no se usan 
        manejar_click_botones(pos, botones_disponibles, botones_usados, estado["palabra_actual"])
        #Esto seria los botones que ya se usaron 
        manejar_click_usados(pos, botones_disponibles, botones_usados, estado["palabra_actual"])
        #por cada boton en botones_accion
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

#Esto le pone condiciones para que el juego termine mostrandote la pantalla de fin y un mensaje
def verificar_fin_juego(estado, tiempo_restante):

    fin = False
    mensaje = ""
    #motivos que detienen  el juego
    if tiempo_restante <= 0:
        fin = True
        mensaje = "tiempo"

    elif len(estado["palabras_encontradas"]) >= len(estado["palabras_validas"]):
        fin = True
        mensaje = "victoria"
    #para que vean los usuarios modo normal, cuanto tiempo les queda
    elif  tiempo_restante <= 10:
        estado["aviso_10"] = True
        mensaje = "Quedan 10 segundos"

    elif tiempo_restante <= 30:
        estado["aviso_30"] = False
        mensaje = "Quedan 30 segundos"

    return fin, mensaje


#Extrae el comodín desde el nivel de la partida.
def obtener_comodin_cambiar_partida(datos_partida):  
    resultado = False
    nivel = datos_partida.get("nivel")
    #Osea que resetea el uso del comodin al cambiar el nivel del juego
    if nivel != None:
        valor = nivel.get("comodin_cambiar_partida")
        if valor != None:
            resultado = valor

    return resultado
   
# Maneja el click sobre los botones de comodines.
def manejar_click_comodines(pos, botones_comodines, comodines_usados, estado):
    
    resultado = None
    #Recorre cada uno de los botones de los comodines
    for b in botones_comodines:
        if b["rect"].collidepoint(pos):
            tipo = b["tipo"]

            if comodines_usados[tipo]:
                break
            #Estaria siendo que segun el tipo de comodin que hay se aplicaria el comodin.
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
