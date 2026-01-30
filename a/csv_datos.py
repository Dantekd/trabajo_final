# MODULO PARA TRABAJAR CON CSV

import csv
import os

# FUNCIONES QUE SE ENCARGAN DE EL FUNCIONAMIENTO DEL CSV EN EL JUEGO.


def cortar_por(cadena: str, separador: str) -> list:
    """Funcion que corta una cadena en partes, usando un separador.

    Args:
        cadena (str): La cadena completa a cortar.
        separador (str): El caracter separador.

    Returns:
        list: Lista con las partes separadas.
    """

    lista = []
    actual = ""
    i = 0

    # recorro caracter por caracter
    while i < len(cadena):
        caracter = cadena[i]

        # si encuentro el separador, guardo la parte actual
        if caracter == separador:
            lista.append(actual)
            actual = ""
        else:
            # sino, sigo acumulando
            actual += caracter

        i += 1

    # agrego el último fragmento
    lista.append(actual)
    return lista


#Se encarga de leer las lineas que hay en el CSV y despues cierra el archivo 

def leer_lineas_csv(ruta: str) -> list:
    """Lee todas las líneas del archivo CSV.

    Args:
        ruta (str): Ruta completa al archivo.

    Returns:
        list: Lista de líneas del archivo.
    """

    archivo = open(ruta, "r", encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()
    return lineas

#Transforma cada linea del CSV en una logica funcional aplicable a la estructura base del juego
def procesar_linea_csv(linea: str) -> dict:
    """Convierte una línea CSV en una estructura de nivel + partida.

    Args:
        linea (str): La línea completa del archivo CSV.

    Returns:
        dict: Diccionario con nivel y datos de la partida.
    """

    # limpio saltos de línea
    linea = linea.strip()

    # separo por columnas
    columnas = cortar_por(linea, ";")

    # convierto tipos de datos
    nivel_num = int(columnas[0])
    base = columnas[1]
    lista_letras = cortar_por(columnas[2], ",")
    lista_validas = cortar_por(columnas[3], "|")

    # creo la partida
    partida = {
        "base": base,
        "letras": lista_letras,
        "validas": lista_validas
    }

    # retorno estructura completa
    resultado = {
        "nivel": nivel_num,
        "partida": partida
    }

    return resultado

#Valida el correcto funcionamiento de niveles y partidas

def nivel_existe(niveles: list, nivel_num: int) -> bool:
    """Indica si un nivel ya existe en la lista de niveles."""

    existe = False
    i = 0

    while i < len(niveles):
        if niveles[i]["nivel"] == nivel_num:
            existe = True
        i += 1

    return existe

#busca el numero del nivel y si al avazar se ve que no existe un siguiente nivel te devuelve -1
def buscar_nivel(niveles: list, nivel_num: int) -> int:
    """Busca el índice de un nivel. Si no existe, devuelve -1."""

    indice = -1
    i = 0

    while i < len(niveles):
        if niveles[i]["nivel"] == nivel_num:
            indice = i
            break
        i += 1

    return indice

#Sirve para la creación/agregado de partidas o niveles, verificando si todavia 
# deben de haber o no, más niveles/partidas.
def agregar_partida_a_niveles(niveles: list, nivel_num: int, partida: dict):
    """Agrega una nueva partida a un nivel existente, o crea el nivel.

    Args:
        niveles (list): Lista de niveles acumulados.
        nivel_num (int): Número del nivel actual.
        partida (dict): Datos de la partida a añadir.
    """

    existe = nivel_existe(niveles, nivel_num)

    # si ya existe, agrego dentro del nivel correspondiente
    if existe:
        indice = buscar_nivel(niveles, nivel_num)
        niveles[indice]["partidas"].append(partida)

    # si no existe, genero el nivel desde cero
    else:
        niveles.append({
            "nivel": nivel_num,
            "partidas": [partida]
        })

#Lee todo el CSV y crea a la estructura de niveles correspondiente según lo que se encuentre en el archivo llamado. 

def leer_csv(ruta: str) -> list:
    """Carga todas las líneas del CSV y arma la estructura de niveles."""

    niveles = []
    lineas = leer_lineas_csv(ruta)

    # empiezo desde 1 porque la primera línea es encabezado
    i = 1
    while i < len(lineas):
        info = procesar_linea_csv(lineas[i])
        agregar_partida_a_niveles(niveles, info["nivel"], info["partida"])
        i += 1

    return niveles

#Sirve para avisar si la base actual ya estuvo dentro del mismo nivel antes.

def base_repetida(bases: list, base_actual: str) -> bool:
    """Indica si una base ya fue vista dentro del mismo nivel."""

    repetida = False
    i = 0

    while i < len(bases):
        if bases[i] == base_actual:
            repetida = True
        i += 1

    return repetida

#Verifica que no haya más de una partida con la misma base en un nivel.

def validar_partidas_nivel(nivel: dict) -> bool:
    """Controla que no existan dos partidas con la misma base en un nivel."""

    bases_vistas = []
    valido = True

    partidas = nivel["partidas"]
    i = 0

    while i < len(partidas):
        base_actual = partidas[i]["base"]

        # si la base ya aparece, está mal
        if base_repetida(bases_vistas, base_actual):
            print("ERROR: Base repetida en nivel:", nivel["nivel"])
            valido = False

        # guardo la base actual para próximas comparaciones
        bases_vistas.append(base_actual)
        i += 1

    return valido

#Recorre todos los niveles haciendo una validación de los correctos y 
# si se encuentra algún error en alguno te devuelve un False.
def validar_niveles(niveles: list) -> bool:
    """Valida todos los niveles. Si alguno tiene error, devuelve False."""

    valido = True
    i = 0

    while i < len(niveles):
        if validar_partidas_nivel(niveles[i]) == False:
            valido = False
        i += 1

    return valido



# Función que se encarga de la carga de datos.


def cargar_niveles():
    """Carga niveles desde el CSV, valida y devuelve la estructura."""

    ruta = os.path.join(os.path.dirname(__file__), "partidas.csv")
    niveles = leer_csv(ruta)
    datos_validos = validar_niveles(niveles)

    # si hubo errores, lo notifica
    if datos_validos == False:
        print("Error en datos del CSV.")

    for nivel in niveles:
        nivel["comodin_cambiar_partida"] = True

    return niveles


def main():
    niveles = cargar_niveles()
