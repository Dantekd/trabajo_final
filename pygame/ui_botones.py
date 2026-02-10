import pygame
#Dimensiones del boton que esta
def crear_botones_letras_csv(letras):
    botones = []
    x = 150
    y = 220
    # Recorre todas las letras recibidas y crea un boton para cada una
    for letra in letras:
        botones.append({
            "letra": letra.upper(),
            "rect": pygame.Rect(x, y, 48, 48),
            "activa": True
        })
        x += 68 #posición de la letra

    return botones

#dimensiones del boton usado
def crear_boton_usado(letra, index):
    boton = {
        "letra": letra,
        "rect": pygame.Rect(150 + index * 68, 315, 48, 48)
    }
    return boton
#Hace el registro de cuando un boton no usado esta disponible o no
def manejar_click_botones(pos, botones_disponibles, botones_usados, palabra_actual):

    for boton in botones_disponibles:
        if boton["activa"] and boton["rect"].collidepoint(pos):#Sirve para identicar si el click esta dentro del area del boton
            boton["activa"] = False
            palabra_actual.append(boton["letra"])
            botones_usados.append(crear_boton_usado(boton["letra"], len(botones_usados))
            )

# Maneja el click sobre los botones usados y permite devolver la letra disponible si el jugador la vuelve a tocar.
def manejar_click_usados(pos, botones_disponibles, botones_usados, palabra_actual):

    i = 0
    #Sirve para condicionar que unicamente pase cuando la cantidad de botones sea mayor que el indice
    while i < len(botones_usados):

        boton = botones_usados[i]
        if boton["rect"].collidepoint(pos):

            letra = boton["letra"]
            palabra_actual.pop(i)
            botones_usados.pop(i)

            for b in botones_disponibles:
                if b["letra"] == letra and not b["activa"]:
                    b["activa"] = True
                    break

            break

        i += 1
#Aca se crean los botones de los comodines  con todas sus caracteristicas
def crear_botones_comodines():

    botones = []
    #Comodin revela parcialmente la palabra
    botones.append({
        "rect": pygame.Rect(150, 400, 170, 40),
        "texto": "Revelar",
        "tipo": "revelar"
    })
    #Comodin ubica letra
    botones.append({
        "rect": pygame.Rect(360, 400, 140, 40),
        "texto": "Ubicar letra",
        "tipo": "ubicar"
    })

    #Boton del comodin 50/50
    botones.append({
        "rect": pygame.Rect(530, 400, 120, 40),
        "texto": "Nivel",
        "tipo": "nivel"
    })

    return botones


def crear_botones_accion():
    botones = []

    botones.append({
        "rect": pygame.Rect(150, 550, 120, 40),
        "accion": "shuffle",
        "texto": "Shuffle"
    })

    botones.append({
        "rect": pygame.Rect(300, 550, 120, 40),
        "accion": "clear",
        "texto": "Clear"
    })

    botones.append({
        "rect": pygame.Rect(450, 550, 120, 40),
        "accion": "submit",
        "texto": "Submit"
    })

    return botones

#“Los botones no se modelaron solo como elementos gráficos, sino como entidades lógicas.
#Por eso, cuando se comportan como un conjunto homogéneo se usan listas, y cuando representan decisiones exclusivas se usan diccionarios.”
def crear_botones_login():
    return {
        "registro": {
            "rect": pygame.Rect(350, 390, 200, 50),
            "texto": "Crear usuario"
        }
    }


def crear_botones_configuracion():
    return {
        "normal": {
            "rect": pygame.Rect(250, 250, 200, 80),
            "texto": "Modo normal"
        },
        "tdah": {
            "rect": pygame.Rect(550, 250, 200, 80),
            "texto": "Modo TDAH"
        }
    }