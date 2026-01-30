# FUNCIONES DE VALIDACIÓN.

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

def controlar_tiempo(tiempo_agotado: bool) -> bool:
    """Funcion que controle un intento de acuerdo a si termino el tiempo.

    Args:
        tiempo_agotado (bool): Si termino el tiempo o no.

    Returns:
        bool: Devuelve si terminó el intento o no.
    """
    # si el tiempo se agotó:
    if tiempo_agotado:
        # intento fallido.
        intento_perdido = True
    else:
        # sino, no.
        intento_perdido = False

    # devuelvo si se perdió o no el intento.
    return intento_perdido

def controlar_partida(intentos_restantes: int) -> bool:
    """Funcion que determina si una partida sigue o no, dependiendo la cantidad de intentos.

    Args:
        intentos_restantes (int): Los intentos restantes.

    Returns:
        bool: Si quedan intentos -> True | Si no quedan intentos -> False.
    """
    # si los intentos restantes son mayores a 0:
    if intentos_restantes > 0:
        # la partida sigue.
        game_over = False
    # sino, no.
    elif intentos_restantes == 0:
        game_over = True

    # devuelvo para terminar el juego.
    return game_over

def verificar_fin_partida(errores: int, max_errores: int, palabras_encontradas: int, total_palabras: int) -> bool:
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

    # perder por errores.
    if errores >= max_errores:
        bandera_estado_partida = True

    # ganar por encontrar todas las palabras.
    if palabras_encontradas >= total_palabras:
        bandera_estado_partida = True

    # devuelvo el bool para verificar.
    return bandera_estado_partida

