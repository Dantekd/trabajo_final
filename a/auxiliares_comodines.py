import random


def elegir_palabra(lista_diccionario: list) -> str:
    """Funcion que elige una palabra random del lista_diccionario.

    Args:
        lista_diccionario (list): La lista tipo diccionario a tomar palabra.

    Returns:
        str: La palabra elegida.
    """
    # variable que se queda con la palabra random.
    palabra_random = random.choice(lista_diccionario)
    # devuelvo la palabra para seguir trabajando con ella.
    return palabra_random

#################################################
# NO SE ESTÁ USANDO POR SI LA RECURSIVA ESTÁ MAL.
def revelar_comodin(palabra: str) -> str:
    """Funcion comodin para revelar letras.

    Args:
        palabra (str): Segun una palabra aleatoria, revela.

    Returns:
        str: Devuelve el comodin 
    """

    # trabajo con una lista vacia -> porque un str es inmutable.
    lista_palabra_revelada = []         
    # la bandera para mostrar o no letra.
    bandera_mostrar = False      

    # recorro 
    for letra in range(len(palabra)):

        if bandera_mostrar:
            lista_palabra_revelada.append(palabra[letra])   
       
        if not bandera_mostrar:
            lista_palabra_revelada.append("_")     
                     
        bandera_mostrar = not bandera_mostrar
    
    palabra_revelada = " ".join(lista_palabra_revelada)

    return palabra_revelada
##################################################

# FUNCION RECURSIVA DE JULIAN.
def revelar_comodin_recursiva(palabra: str, resultado: list = None, bandera_mostrar: bool = False, indice: int = 0) -> list:
    """Funcion comodin para revelar letras. RECURSIVA.

    Args:
        palabra (str): Segun una palabra aleatoria, revela.
        resultado (list, optional): Lista que acumula las letras procesadas. Defaults to None. Si se pasa un parametro falla la recursividad. DEJAR ASÍ.
        bandera_mostrar (bool, optional): Bandera que indica si se muestra o no la letra. Defaults to False. Si se pasa un parametro falla la recursividad. DEJAR ASÍ.
        indice (int, optional): Posicion actual dentro de la palabra. Defaults to 0. Si se pasa un parametro falla la recursividad. DEJAR ASÍ.

    La idea de hacerla recursiva era para eliminar el bucle interno de la funcion y que se llame a si misma para ir descomponiendo el problema
    hasta el caso mas minimo -- En este caso, la ultima letra de la palabra, y revelarla o no, dependiendo si tocaba guion o letra.    
    
    Returns:
        list: Devuelve la palabra parcialmente revelada. COMODIN.
    """

    # inicio la recursividad.
    if resultado == None:
        # la lista vacia será nuestro acumulador.
        resultado = []  
    
    # recorro a partir del indice.
    if indice < len(palabra):  
        # si el bool es True:
        if bandera_mostrar:
            # muestra la letra.
            resultado.append(palabra[indice])
        else:
            # sino, la oculta con un guion.
            resultado.append("_")
        # todo esto sumando a la lista...

        # llamada recursiva para recorrer hasta el ultimo caracter.
        revelar_comodin_recursiva(palabra, resultado, not bandera_mostrar, indice + 1)
    palabra_revelada = " ".join(resultado)
    # devuelvo el "comodin", sin espacios.
    return palabra_revelada


def revelar_letra_en_palabra(palabra: str, letra: str) -> str:
    """Funcion para revelar una letra en una palabra.

    Args:
        palabra (str): La palabra a "revelar"
        letra (str): La letra a mostrar.

    Returns:
        str: Devuelve la palabra oculta con la letra aleatoria visible.
    """
    # incializo:
    revelada = []
    k = 0

    # recorro y concateno:
    while k < len(palabra):
        if palabra[k] == letra:
            revelada.append(letra.upper())
        else:
            revelada.append("_")
        k += 1

    # devuelvo sin espaciado para seguir trabajando.
    palabra_revelada = " ".join(revelada)
    return palabra_revelada

def revelar_letra_en_listado(letra: str, palabras_validas: list, palabras_encontradas: list) -> list:
    """Funcion que revela una letra en todas las palabras no encontradas.

    Args:
        letra (str): La letra a insertar.
        palabras_validas (list): La lista de palabras validas.
        palabras_encontradas (list): La lista de palabras encontradas.

    Returns:
        list: Devuelve una lista con todas las palabras no encontradas y la letra en cuestión.
    """
    # creo una lista vacia.
    lista_resultado = []
   
    for i in range(len(palabras_validas)):
        palabra = palabras_validas[i]

        # si no pertenece, sumo a la lista todas las palabras "reveladas".
        if not buscar_palabra_ya_encontrada(palabra, palabras_encontradas):
            revelada = revelar_letra_en_palabra(palabra, letra)  
            lista_resultado.append(revelada)

    # devuelvo la lista resultado con todas las palabras "reveladas".
    return lista_resultado

def revisar_letra_valida_palabra_no_encontrada(letra: str, palabras_validas: list, palabras_encontradas: list) -> bool:
    """Funcion que busca si una letra segun palabra no encontrada es valida. 

    Args:
        letra (str): La letra a buscar.
        palabras_validas (list): La lista de palabras validas.
        palabras_encontradas (list): La lista de palabras encontradas.

    Returns:
        bool: Devuelve True si si sirve | False si no.
    """

    # inicializo y recorro.
    bandera_sirve = False

    for i in range(len(palabras_validas)):
        palabra = palabras_validas[i]

        # si sirve...
        if not buscar_palabra_ya_encontrada(palabra, palabras_encontradas):
            if verificar_letra_en_palabra(letra, palabra):
                bandera_sirve = True

    # devuelvo el bool para seguir trabajando.
    return bandera_sirve

# FUNCION DE ORDENAMIENTO DE JULIAN.
# METODO DE ORDENAMIENTO: SELECCION SORT.
def ordenar_palabras_por_longitud(lista_palabras: list) -> list:
    """Funcion que ordena palabras de menor a mayor segun longitud.

    Args:
        lista_palabras (list): La lista de palabras a ordenar.

    Returns:
        list: La lista ordenada.
    """
    # recorro la lista de palabras.
    for i in range(len(lista_palabras)):
        # incializo suponiendo que el minimo de longitud es donde esta i.
        indice_minimo = i
        # recorro la lista de palabras + 1, es decir, el "recorrido" para hacer el ordenamiento.
        for j in range(i + 1, len(lista_palabras)):
            # si el largo de la palabra en el segundo recorrido es menor al primero:
            if len(lista_palabras[j]) < len(lista_palabras[indice_minimo]):
                # reemplazo el minimo.
                indice_minimo = j

        # e intercambio el elemento actual con el minimo encontrado.
        # asigno la palabra en i a una variable temporal.
        temporal = lista_palabras[i]
        # a esa palabra en i la reemplazo por la palabra con el minimo encontrado.
        lista_palabras[i] = lista_palabras[indice_minimo]
        # luego reemplazo para aplicar el ordenamiento.
        lista_palabras[indice_minimo] = temporal

    # devuelvo la lista de palabras ordenadas.
    return lista_palabras


def burbujear_por_longitud(lista_palabras: list) -> list:

    for i in range(len(lista_palabras)):
        for j in range(0, len(lista_palabras) - 1 - i):
            if len(lista_palabras[j]) > len(lista_palabras[j + 1]):
                # Intercambio
                temporal = lista_palabras[j]
                lista_palabras[j] = lista_palabras[j + 1]
                lista_palabras[j + 1] = temporal
                
    return lista_palabras

def verificar_letra_en_palabra(letra: str, palabra: str) -> bool:
    """Funcion que verifica si una letra aparece en una palabra.

    Args:
        letra (str): La letra a buscar.
        palabra (str): La palabra donde buscar.

    Returns:
        bool: Devuelve True si la encuentra | False si no.
    """
    # inicializo y recorro.
    bandero_encontro = False

    for i in range(len(palabra)):
        # si la encuentra:
        if palabra[i] == letra:
            bandero_encontro = True

    # devuelvo el bool para seguir trabajando.
    return bandero_encontro


def buscar_palabra_ya_encontrada(palabra: str, encontradas: list) -> bool:
    """Funcion para buscar si una palabra ya fue revelada.

    Args:
        palabra (str): La palabra a buscar.
        encontradas (list): La lista de palabras encontradas.

    Returns:
        bool: Devuelve un bool para seguir trabajando.
    """
    # inicializo y recorro.
    bandera_encontrada = False

    for j in range(len(encontradas)):
        if palabra == encontradas[j]:
            bandera_encontrada = True

    # devuelvo para seguir trabajando.
    return bandera_encontrada

# MODULO PARA MINIFICAR LAS FUNCIONES DEL FLUJO JUEGO.

def obtener_accion(resultado) -> str | None:
    """
    Si el resultado es dict y tiene la clave 'accion', devuelve su valor.
    Caso contrario devuelve None.
    """

    # inicializo la variable por defecto.
    valor = None

    if type(resultado) == dict:
        temporal = resultado.get("accion")

        if temporal != None:
            valor = temporal

    return valor

def manejar_cambiar_partida(nivel: dict):
    """
    Marca como gastado el comodín cambiar_partida en el nivel.
    """
    # cambio el valor bool para gastar el comodin.
    nivel["comodin_cambiar_partida"] = False


def procesar_resultado_partida(resultado, nivel):
    """
    Procesa el resultado de jugar_partida:
      - Detecta salir
      - Detecta acción cambiar_partida
      - Retorna ('salir', None)
      - Retorna ('accion', 'cambiar_partida')
      - Retorna ('puntaje', valor)
    """

    respuesta = ("puntaje", resultado)  # valor por defecto

    # 1) salir
    if resultado == "salir":
        respuesta = ("salir", None)

    else:
        # 2) acción (si la hay)
        accion = obtener_accion(resultado)
        if accion != None:
            if accion == "cambiar_partida":
                manejar_cambiar_partida(nivel)
                respuesta = ("accion", "cambiar_partida")

    return respuesta

def buscar_si_tiene_clave(diccionario, clave):

    claves = list(diccionario.keys())

    bandera_tiene = False

    for i in range(len(claves)):
        if claves[i] == clave:
            bandera_tiene = True

    return bandera_tiene


def gastar_comodin_cambiar_partida(datos_partida):
    if buscar_si_tiene_clave(datos_partida, "nivel"):
        nivel = datos_partida["nivel"]
        if nivel != None:
            manejar_cambiar_partida(nivel)



def interpretar_resultado_opcion(resultado, estado, datos_partida):
    
    tipo = "seguir"
    valor = None

    # Caso salir
    if resultado == "salir":
        tipo = "salir"

    else:
        # Caso acción
        accion = obtener_accion(resultado)

        if accion != None:
            if accion == "cambiar_partida":
                gastar_comodin_cambiar_partida(datos_partida)
                tipo = "accion"
                valor = "cambiar_partida"
        else:
            # Caso fin de partida normal
            if resultado == False:
                tipo = "fin_normal"

    return (tipo, valor)
