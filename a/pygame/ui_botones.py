import pygame
#Dimensiones del boton que esta
def crear_botones_letras_csv(letras):
    botones = []
    x = 300
    y = 220

    for letra in letras:
        botones.append({
            "letra": letra.upper(),
            "rect": pygame.Rect(x, y, 48, 48),
            "activa": True
        })
        x += 68

    return botones
#dimensiones del boton usado
def crear_boton_usado(letra, index):
    boton = {
        "letra": letra,
        "rect": pygame.Rect(300 + index * 68, 310, 48, 48)
    }
    return boton

