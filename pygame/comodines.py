# comodines.py
import random

def comodin_revelar_palabra(estado):
    restantes = []

    for p in estado["palabras_validas"]:
        if p not in estado["palabras_encontradas"]:
            restantes.append(p)

    parcial = ""

    if len(restantes) > 0:
        palabra = random.choice(restantes)
        mitad = len(palabra) // 2
        parcial = palabra[:mitad] + "_," * (len(palabra) - mitad)

    return parcial


   
def comodin_ubicar_letra(estado):
    """
    Selecciona una letra que aparezca en todas las palabras restantes
    y la devuelve para ser mostrada al jugador.
    """
    restantes = []

    for p in estado["palabras_validas"]:
        if p not in estado["palabras_encontradas"]:
            restantes.append(p)

    letra = None

    if len(restantes) > 0:
        comunes = set(restantes[0])

        for palabra in restantes[1:]:
            comunes = comunes.intersection(set(palabra))

        if len(comunes) > 0:
            letra = random.choice(list(comunes))

    return letra


def comodin_nivel():
    numero = random.randint(0, 1)

    accion = "subir"
    if numero == 0:
        accion = "bajar"

    return accion



