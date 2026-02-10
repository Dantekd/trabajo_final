from login_pygame import *
from nucleo_juego import preparar_partida
from numericas import sumar_puntaje, acumular_ingresos_incorrectos
from ui_botones import *

#Esto representaria como las reglas del juego

#Esto crea lo datos que puede llegar a haber dentro del juego osea las estadisticas generales
def crear_estado_pygame(base_lista, palabras_validas, perfil):
    estado = {
        "base_lista": base_lista,
        "palabras_validas": palabras_validas,
        "palabras_encontradas": [],
        "palabras_ingresadas": [],
        "palabras_invalidas": [], 
        "palabra_actual": [],
        "puntaje": 0,
        "errores": 0,
        "mensaje_":"",
        "mensaje_timer":0,
        "intentos_maximos": 5,
        "tiempo_restante": 60,
        "ultimo_resultado": "",
        "comodines": {
            "revelar": True,
            "ubicar": True,
            "cincuenta": True
        },
        "perfil": perfil
    }
    return estado

#Esto precesa la cantidad de palabra aun no descubiertas.
def procesar_palabra_pygame(estado, palabra):
    resultado = ""

    palabra_minus = palabra.lower()
    repetida = False

    i = 0
    while i < len(estado["palabras_ingresadas"]):#hace que el contador aumente de si llegaste a descubrir una palabra correcta
        if estado["palabras_ingresadas"][i] == palabra_minus:
            repetida = True
        i = i + 1

    if repetida:
        resultado = "repetida"
    #palabra_minus saber explicar
    else:
        es_valida = validar_palabra(#Esto valida si la palabra que se ingresa esra dentro 
            palabra_minus,
            estado["base_lista"],
            estado["palabras_validas"]
        )

        if es_valida:
            estado["puntaje"] = sumar_puntaje(estado["puntaje"], palabra_minus)
            estado["palabras_encontradas"].append(palabra_minus)
            resultado = "valida"
        else:
            estado["errores"] = acumular_ingresos_incorrectos(
                estado["errores"],es_valida
            )
            resultado = "invalida"

        estado["palabras_ingresadas"].append(palabra_minus)

    estado["ultimo_resultado"] = resultado
    return resultado


#Función que a partir de una lista de letras, comprueba si una palabra existe.
def buscar_puede_formarse(palabra: str, letras: list) -> bool:
    # genera una copia de la lista para trabajar y poder eliminar, si se requiere.
    letras_disponibles = list(letras)  
    # inicializo bandera para retornar.
    bandera_validacion = True

    # recorro, inicializo y comparo.
    for i in range(len(palabra)):
        letra_encontrada = False
        for j in range(len(letras_disponibles)): # NO COMPRENSIO NDE LISTAS
            if letras_disponibles[j] == palabra[i]:
                # elimino la letra usada, en caso de que haya repetición.
                letras_disponibles.remove(letras_disponibles[j])  
                letra_encontrada = True
                break
        # si no la encuentra == False.
        if letra_encontrada == False:
            bandera_validacion = False
            break
  
    return bandera_validacion
#Busca la palabra dentro de un diccionario.
def buscar_palabra_diccionario(palabra: str, diccionario_palabras: list) -> bool:
    bandera_diccionario = False

    for i in range(len(diccionario_palabras)):
        if palabra == diccionario_palabras[i]:
            bandera_diccionario = True
            break

    return bandera_diccionario

#Verifica si las letras y la palabra pertenecen a las listas
def validar_palabra(palabra: str, letras: list, diccionario: list) -> bool:
    bandera_validacion = False 

    if buscar_puede_formarse(palabra, letras):
        if buscar_palabra_diccionario(palabra, diccionario):
            bandera_validacion = True

    return bandera_validacion
