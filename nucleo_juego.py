# MODULO CON TODA LA LOGICA DEL JUEGO.

import random

from mecanicas import normalizar_lista_base_minusculas, quitar_duplicados_lista_a_set, desordenar_letras, ajustar_letras





def preparar_partida(datos_partida: dict) -> tuple:
    """Funcion para preparar la partida.

    Args:
        datos_partida (dict): Los datos del diccionario.

    Returns:
        tuple: Devuelve tupla, para seguir trabajando.
    """
    # asigno variables.
    base = datos_partida["base"]
    base_lista_original = datos_partida["letras"]
    palabras_validas = datos_partida["validas"]

    # paso todo a minuscula.
    base_lista = normalizar_lista_base_minusculas(base_lista_original)

    # convierto a set.
    base_set = quitar_duplicados_lista_a_set(base_lista)

    # devuelvo tupla, para seguir trabajando.
    return base_set, base_lista, palabras_validas



# inicializo un diccionario para recordar que partidas ya salieron por nivel.
partidas_usadas_por_nivel = {}  


def verificar_partida_registrada(numero_nivel: int) -> bool:
    """Funcion que verifica si una partida existe dentro del dict "usadas por nivel""

    Args:
        numero_nivel (int): El numero del nivel.

    Returns:
        bool: Devuelve True si existe | False si no.
    """
    # creo una lista a partir del dict y me quedo con sus keys.
    claves = list(partidas_usadas_por_nivel.keys())
    # inicializo y recorro.
    bandera_existe = False

    for i in range(len(claves)):
        # si existe...
        if claves[i] == numero_nivel:
            bandera_existe = True

    # devuelvo el bool para seguir trabajando.
    return bandera_existe


def reiniciar_si_completo(numero_nivel: int, partidas: list) -> None:
    """Funcion que reinicia la "busqueda" si se completaron todas las partidas de un nivel.

    Args:
        numero_nivel (int): El numero del nivel.
        partidas (list): La lista de partidas del nivel.
    """
    # defino las partidas que ya se usaron.
    usadas = partidas_usadas_por_nivel[numero_nivel]

    # si se usaron todas, se reinicia la lista para volver a jugar las partidas.
    if len(usadas) == len(partidas):
        partidas_usadas_por_nivel[numero_nivel] = []


def verificar_repeticion_valor(lista: list, valor: int) -> bool:
    """Funcion que verifica si un valor se repite dentro de una lista.

    Args:
        lista (list): La lista a evaluar.
        valor (int): El valor a buscar.

    Returns:
        bool: Devuelve True si se repite | False si no.
    """
    # inicializo y recorro.
    bandera_repite = False

    for i in range(len(lista)):
        # si se repite:
        if lista[i] == valor:
            bandera_repite = True

    return bandera_repite



def obtener_indice_aleatorio_no_usado(numero_nivel: int, partidas: list) -> int:
    """Funcion que obtiene el indice aleatorio no usado para los niveles.

    Args:
        numero_nivel (int): _description_
        partidas (list): _description_

    Returns:
        int: _description_
    """
    # defino la lista de las partidas usadas.
    usadas = partidas_usadas_por_nivel[numero_nivel]

    # inicializo y recorro.
    idx = -1
    valido = False


    while not valido:
        # le dedico al indice un int aleatorio.
        idx = random.randint(0, len(partidas)-1)
        # sino se repite...
        if not verificar_repeticion_valor(usadas, idx):   
            valido = True

    return idx


def buscar_partida_aleatoria_sin_repetir(nivel: dict) -> dict:
    """Funcion que elige una partida aleatoria dentro de un nivel sin repetir hasta usar todas.

    Args:
        nivel (dict): Debe ser:
            {
                "nivel": int,
                "partidas": [ { datos_partida_1 }, { datos_partida_2 }, ... ]
            }

    Returns:
        dict: Devuelve una partida aleatoria aun no repetida.
    """
    # defino el numero del nivel.
    numero_nivel = nivel["nivel"]
    # lista de partidas disponibles. 
    partidas = nivel["partidas"]

    # verifico si el nivel ya existe en el historial.
    # sino, creo una lista nueva.
    if not verificar_partida_registrada(numero_nivel):
        partidas_usadas_por_nivel[numero_nivel] = []

     # si ya usamos todas las partida -> se reinicia
    reiniciar_si_completo(numero_nivel, partidas)

    # y ahora, a elegir un indice que no esté repetido.
    indice = obtener_indice_aleatorio_no_usado(numero_nivel, partidas)

    # lo guardamos para evitar repetirlo.
    partidas_usadas_por_nivel[numero_nivel].append(indice)

    partida_seleccionada = partidas[indice]
    partida_seleccionada = partidas[indice].copy()
    partida_seleccionada["comodin_cambiar_partida"] = nivel["comodin_cambiar_partida"]
    
    return partida_seleccionada

