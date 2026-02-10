import random
#Funcionamiento del comodin revelar
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


#Funcionamiento del comodin ubicar.
def comodin_ubicar_letra(estado):
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


#Función 50/50 que es más logica de partida 

def comodin_nivel():
    numero = random.randint(0, 1)

    accion = "subir"
    if numero == 0:
        accion = "bajar"

    return accion



