#CONTADOR DE COSAS PARA VER: 2
from numericas import sumar_puntaje, acumular_ingresos_incorrectos

#Esto crea lo datos que puede llegar a haber dentro del juego osea las estadisticas generales
#Osea que serian como las reglas del juego
def crear_estado_pygame(base_lista, palabras_validas, perfil):
    estado = {
        "base_lista": base_lista,
        "palabras_validas": palabras_validas,
        "palabras_encontradas": [],
        "palabras_ingresadas": [],
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
    while i < len(estado["palabras_ingresadas"]):#hace que el contador disminuya de si llegaste a descubrir una palabra correcta
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


def verificar_fin_pygame(estado):
    terminado = False

    if estado["errores"] >= estado["intentos_maximos"]:
        terminado = True

    if len(estado["palabras_encontradas"]) >= len(estado["palabras_validas"]):
        terminado = True

    return terminado


#Lo nuevo 
 
def buscar_puede_formarse(palabra: str, letras: list) -> bool: #anotacion de Dante esto puede servir para cuando quiera reemplazar la palabra en los espaciados
    """Funcion que a partir de una lista de letras, comprueba si una palabra existe.

    Args:
        palabra (str): La palabra a evaluar.
        letras (list): La lista de letras a comparar.

    Returns:
        bool: Validación. True si cumple | False si no.
    """
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
    # retorna la validacion para trabajar.
    return bandera_validacion

def buscar_palabra_diccionario(palabra: str, diccionario_palabras: list) -> bool:
    """Funcion que busca la palabra dentro de un diccionario.

    Args:
        palabra (str): La palabra a buscar.
        diccionario (list): El diccionario donde buscar la palabra.

    Returns:
        bool: Devuelve True si la encuentra | False si no.
    """
    # inicializo.
    bandera_diccionario = False

    # recorro, si encuentro, == True. NO COMPRENSION DE LISTAS.
    for i in range(len(diccionario_palabras)):
        if palabra == diccionario_palabras[i]:
            bandera_diccionario = True
            break

    # sino, queda False.
    return bandera_diccionario

def validar_palabra(palabra: str, letras: list, diccionario: list) -> bool:
    """Funcion que verifica si las letras y la palabra pertenecen a las listas.

    Args:
        palabra (str): La palabra a evaluar.
        letras (list): Letras disponibles para formar palabras.
        diccionario (list): Lista de palabras válidas.

    Returns:
        bool: True si se puede formar y está en el diccionario | False si no.
    """
    # inicializo para devolver el bool.
    bandera_validacion = False    
    # si puede formarse con las letras.
    if buscar_puede_formarse(palabra, letras):
        # y existe en el diccionario.
        if buscar_palabra_diccionario(palabra, diccionario):
            bandera_validacion = True

    # devuelvo para seguir trabajando con el bool. -> esto sería ya para para el puntaje??
    return bandera_validacion


def verificar_fin_partida(palabras_encontradas: int, total_palabras: int) -> bool:
    """Funcion que verifica el estado de la partida.

    Args:
        errores (int): Los errores acumulados.
        max_errores (int): El maximo de errores.
        palabras_encontradas (int): Las palabras encontradas.
        total_palabras (int): El total de palabras restantes.

    Returns:
        bool: Devuelve el bool. True si termina | False si sigue.
    """

    # inicializo la bandera para seguir jugando.
    bandera_estado_partida = False

    # ganar por encontrar todas las palabras.
    if palabras_encontradas >= total_palabras:
        bandera_estado_partida = True

    # devuelvo el bool para verificar.
    return bandera_estado_partida
