# FUNCIONES QUE DEVUELVEN UN NUMERO, REALIZAN OPERACIONES Y/O ACUMULAN.

# FUNCION PARA CALCULAR EL PUNTAJE, FALTA VALIDAR O LINKEARLA CON LAS FUNCIONES DE VALIDACION.
def calcular_puntaje(palabra: str) -> int:
    """Funcion que a partir de una cantidad de letras, calcula un puntaje.

    Args:
        palabra (str): La palabra a evaluar.

    Returns:
        int: Devuelve un int para sumar.
    """

    # el puntaje será el largo de la palabra, valiendo cada letra 1 punto.
    puntaje = len(palabra)

    # devuelve el puntaje.
    return puntaje

# mismo, pero suma el puntaje anterior con uno nuevo.
def sumar_puntaje(puntaje_actual: int, palabra: str) -> int:
    """Funcion que suma puntaje al puntaje actual.

    Args:
        puntaje_actual (int): Puntaje actual antes de sumar.
        palabra (str): La palabra nueva a sumar.

    Returns:
        int: Devuelve la suma.
    """

    # a partir del puntaje, suma el nuevo.
    nuevo_puntaje = puntaje_actual + calcular_puntaje(palabra)

    # devuelvo para seguir trabajando.
    return nuevo_puntaje

def controlar_intentos(intentos_restantes: int, intento_perdido: bool) -> int:
    """Funcion que controla los intentos.

    Args:
        intentos_restantes (int): Los intentos restantes de la partida.
        intento_perdido (bool): Si es un intento perdido: resta.

    Returns:
        int: Devuelve los intentos restantes.
    """
    # si se perdió un intento.
    if intento_perdido:
        # se resta de los intentos restantes.
        intentos_restantes -= 1
        # sino, no.
    elif intento_perdido == False:
        intentos_restantes = intentos_restantes

    # devuelvo los intentos restantes.
    return intentos_restantes

# FUNCION PARA ESTADISTICAS.

def acumular_ingresos_incorrectos(contador_actual: int, palabra_valida: bool) -> int:
    """Funcion que acumula los ingresos incorrectos.

    Args:
        contador_actual (int): El contador actual de ingresos incorrectos.
        palabra_valida (bool): Si la palabra es valida o no.

    Returns:
        int: Devuelve la cantidad de ingresos incorrectos.
    """
    
    # contador respecto al contador actual -> segun variable.
    nuevo_contador = contador_actual

    # si la validacion de la palabra da False:
    if palabra_valida == False:
        # se suma 1 al contador de los ingresos incorrectos.
        nuevo_contador += 1

    # devuelvo la cantidad de ingresos incorrectos.
    return nuevo_contador