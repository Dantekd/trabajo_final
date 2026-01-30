from auxiliares_comodines import buscar_palabra_ya_encontrada, revelar_letra_en_listado, revisar_letra_valida_palabra_no_encontrada, ordenar_palabras_por_longitud, elegir_palabra, revelar_comodin_recursiva
import random


def usar_comodin_ubicar_letra(base_lista: list, palabras_validas: list, palabras_encontradas: list) -> list:
    """Funcion que usa el comodin ubicar letra para todas las palabras NO encontradas.

    Args:
        base_lista (list): La lista de bases a utilizar.
        palabras_validas (list): La lista de palabras validas.
        palabras_encontradas (list): La lista de palabras encontradas.

    Returns:
        list: Devuelve una lista con todas las palabras "reveladas"
    """

    # creo una cadena vacia.
    letra_random = ""
    
    # asigno una letra random segun la lista de bases.
    while letra_random == "":
        letra_candidata = random.choice(base_lista)

        # si me sirve, la reemplazo por la cadena vacia.
        if revisar_letra_valida_palabra_no_encontrada(letra_candidata, palabras_validas, palabras_encontradas):
            letra_random = letra_candidata

    # ORDENAMIENTO APLICADO.
    # creo una copia de las palabras validas para no modificar esa lista.
    # si lo piden, podria hacer el copy afuera.
    palabras_ordenadas = ordenar_palabras_por_longitud(palabras_validas.copy())

    # asi con todas las que pueda, asigno a una lista.
    palabras_reveladas = revelar_letra_en_listado(letra_random, palabras_ordenadas, palabras_encontradas)

    # y devuelvo la lista para revelar el comodin.
    return palabras_reveladas

def usar_comodin_revelar_palabra(lista_diccionario: list, palabras_encontradas: list) -> list:
    """
    Activa el comodín de revelar palabra.

    Returns:
        (str, str): palabra original y palabra parcialmente revelada.
    """
    # creo una cadena vacia.
    palabra = ""

    # la recorro.
    while palabra == "":
        palabra_candidata = elegir_palabra(lista_diccionario)

        # si aun no fue encontrada -> la uso
        if not buscar_palabra_ya_encontrada(palabra_candidata, palabras_encontradas):
            palabra = palabra_candidata
    
    # la revelo parcialmente.
    revelada = revelar_comodin_recursiva(palabra)
    # devuelvo ambos, para seguir trabajando.
    return  revelada

def obtener_comodin_cambiar_partida(datos_partida):
    """Extrae el comodín desde el nivel de la partida, con validación."""
    
    resultado = False

    nivel = datos_partida.get("nivel")
    if nivel != None:
        valor = nivel.get("comodin_cambiar_partida")
        if valor != None:
            resultado = valor

    return resultado

