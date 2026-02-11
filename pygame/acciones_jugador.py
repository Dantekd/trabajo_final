# acciones_jugador.py
from numericas import sumar_puntaje, acumular_ingresos_incorrectos
from nucleo_pygame import procesar_palabra_pygame,validar_palabra
import random
import pygame
from ui_botones import *

#Lo que sucede al accionar shuffle
def accion_shuffle(letras):
    letras_mezcladas = list(letras)
    random.shuffle(letras_mezcladas)
    return letras_mezcladas


def accion_clear(estado):
    estado["palabra_actual"] = []
    return estado


def accion_submit(estado):
    #join se usa para unir una lista con un texto
    palabra = "".join(estado["palabra_actual"]).lower()
    resultado = ""

    repetida = False
    for p in estado["palabras_ingresadas"]:
        if p == palabra:
            repetida = True

    if repetida:
        resultado = "repetida"
    else:
        valida = validar_palabra(
            palabra,
            estado["base_lista"],
            estado["palabras_validas"]
        )

        if valida:
            estado["puntaje"] = sumar_puntaje(estado["puntaje"], palabra)
            estado["palabras_encontradas"].append(palabra)
            resultado = "valida"
        else:
            estado["errores"] = acumular_ingresos_incorrectos(
                estado["errores"], False
            )
            resultado = "invalida"

        estado["palabras_ingresadas"].append(palabra)

    estado["palabra_actual"] = []
    estado["ultimo_resultado"] = resultado

    return estado

#Esto sirve para al ingresar la palabra que sucede
def accion_submit(estado, botones_usados, botones_disponibles):
    palabra = "".join(estado["palabra_actual"])
    resultado = procesar_palabra_pygame(estado, palabra)

    # Muestra los mensajes solo con modo tdah
    if estado.get("tdah", False):
        if resultado == "repetida":
            estado["mensaje"] = "Ya ingresaste esa palabra"
            estado["mensaje_timer"] = 2

        elif resultado == "invalida":
            estado["mensaje"] = "Palabra incorrecta"
            estado["mensaje_timer"] = 2

        elif resultado == "valida":
            estado["mensaje"] = "¡Palabra correcta!"
            estado["mensaje_timer"] = 2

    # Reactivar letras usadas
    for boton_usado in botones_usados:
        letra = boton_usado["letra"]
        for b in botones_disponibles:
            if b["letra"] == letra:
                b["activa"] = True
                break

    estado["palabra_actual"].clear()
    botones_usados.clear()

    for b in botones_disponibles:
        b["activa"] = True

    
#Funcionamiento del Clear
def accion_clear(estado, botones_usados, botones_disponibles):
    estado["palabra_actual"].clear()

    for b in botones_disponibles:
        b["activa"] = True

    botones_usados.clear()

#Funcionamiento del shuffle
def accion_shuffle(botones_disponibles):
    letras = [b["letra"] for b in botones_disponibles]
    random.shuffle(letras)

    botones_disponibles.clear()
    botones_disponibles.extend(crear_botones_letras_csv(letras))

#Llama a todas las acciones de palabras.
def manejar_accion_jugador(accion, estado, botones_usados, botones_disponibles):

    if accion == "submit":
        accion_submit(estado, botones_usados, botones_disponibles)

    elif accion == "clear":
        accion_clear(estado, botones_usados, botones_disponibles)

    elif accion == "shuffle":
        accion_shuffle(botones_disponibles)

    return estado
#Detecta las teclas y ejecuta para las acciones de palabras
def detectar_accion_teclado(evento):

    accion = None

    if evento.key == pygame.K_RETURN:
        accion = "submit"

    elif evento.key == pygame.K_BACKSPACE:
        accion = "clear"

    elif evento.key == pygame.K_SPACE:
        accion = "shuffle"

    return accion