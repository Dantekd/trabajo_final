# FUNCIONES MECANICAS, HACEN UNA FUNCION Y EN GENERAL, TRANSFORMAN "ALGO".
import random
# OPCION SHUFFLE.
# funcion para un boton futuro de desordenar y ayudarse?
def desordenar_letras(letras: list) -> list:
    """Funcion que desordena los elementos de una lista.

    Args:
        letras (list): La lista de letras a desordenar.

    Returns:
        list: Devuelve la lista desordenada.
    """
    # hacemos una copia para no modificar la lista original.
    letras_desordenadas = list(letras)  
    # la desordenamos random.
    random.shuffle(letras_desordenadas)  
    # devolvemos la lista desordenada.
    return letras_desordenadas

# MAYUS
# funcion para mostrar las letras, en consola con print y en pygame con...
def ajustar_letras(letras: list) -> str:
    """Funcion que a partir de una lista, devuelve las letras concatenadas.

    Args:
        letras (list): La lista a manejar.

    Returns:
        str: La cadena de letras para usar.
    """

    # inicializo una cadena vacía.
    resultado = ""
    # recorro la lista.
    for i in range(len(letras)):
        # concateno la lista con cada letra en mayuscula.
        resultado += letras[i].upper()
       # devuelvo la lista de letras en una cadena en mayus. 
    return resultado



def normalizar_lista_base_minusculas(base: list) -> list:
    """Funcion que pasa el formato de la base a minusculas.

    Args:
        base (list): La base a convertir.

    Returns:
        list: Devuelta la lista en minusculas.
    """
    # genero una nueva lista, vacía.
    resultado = []

    # recorro la base:
    for i in range(len(base)):
        # asigno la letra y la convierto en minuscula.
        letra_minus = base[i].lower()
        # las voy añadiendo en la nueva lista.
        resultado.append(letra_minus)

    # devuelvo la lista en minusculas.
    return resultado


def quitar_duplicados_lista_a_set(lista: list) -> set:
    """Funcion que a partir de una lista, la convierte en set.

    Args:
        lista (list): La lista a trabajar.

    Returns:
        set: Devuelve el set de la lista.
    """
    # genero un set vacio.
    resultado = set()

    # recorro la lista:
    for i in range(len(lista)):
        # añado los elementos al set.
        resultado.add(lista[i])

    # devuelvo el set para seguir trabajando sin duplicados.
    return resultado



def normalizar_base_str(palabra: str) -> list:
    """Funcion que pasa un str a una lista.

    Args:
        palabra (str): La palabra a convertir.

    Returns:
        list: La palabra convertida en una lista.
    """
    # creo una lista vacia.
    resultado = []
    # recorro el str:
    for i in range(len(palabra)):
        # armo la lista con cada caracter del str.
        resultado.append(palabra[i].lower())

    # devuelvo la lista, para trabajar.    
    return resultado


def generar_guiones(palabra: str) -> str:
    """Funcion para generar los guiones de la palabra "base".

    Args:
        palabra (str): La palabra a "ocultar" con guiones.

    Returns:
        str: El str conformado por guiones.
    """
    # creo una cadena vacia.
    resultado = ""

    # recorro la palabra:
    for i in range(len(palabra)):
        # concateno la cadena vacia con los guiones
        resultado += "_ "
    # devuelvo ->
    return resultado.strip()  # quita el espacio final



def ordenar_minimo(lista):
    """Consigue el minimo 

    Args:
        lista (_type_): ordena de menor a mayor

    Returns:
        _type_: devuelve el minimo
    """
    i = 0
    minimo = 0  # arranco suponiendo que el mínimo es el primero

    while i < len(lista):
        if lista[i] < lista[minimo]:
            minimo = i
        i += 1

    return minimo

def imprimir_lista(lista):

    for i in range(len(lista)):
        print(lista[i])
        

def buscar_palabra_ya_ingresada(lista, palabra):
    i = 0
    repetida = False

    for i in range(len(lista)):
        if lista[i] == palabra:
            repetida = True
       
       
    return repetida




