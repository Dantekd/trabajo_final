import pygame

from pygame.locals import *

def dibujar_vertical_degradado(surface, top_color, bottom_color):
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        # Interpolación lineal del color
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

#configuracion predeterminada de el fondo
ANCHO_PANTALLA = 900
ALTO_PANTALLA = 500
COLOR_FONDO = (30, 30, 30)
COLOR_TEXTO = (255, 255, 255)
FUENTE_TAM = 32

# =============================
# INICIALIZACIÓN
# =============================


# =============================
# FUNCIONES MODULARES
# =============================
def dibujar_texto(superficie, texto, x, y):
    """Dibuja texto en la superficie."""
    imagen = fuente.render(texto, True, COLOR_TEXTO)
    superficie.blit(imagen, (x, y))
    return None  # Único return

def obtener_evento_tecla():
    """Devuelve una letra presionada o '__SALIR__' o None."""
    salida = None  # Valor por defecto
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == QUIT:
            salida = "__SALIR__"
            break
        else:
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    salida = "__SALIR__"
                    break
                else:
                    tecla = evento.unicode
                    if tecla.isalpha():
                        salida = tecla.upper()
                        break
    return salida  # Único return

def mostrar_interfaz(base, letras, palabra_actual, nivel):
    """Dibuja toda la interfaz del juego en pantalla."""
    pantalla.fill(COLOR_FONDO)

    # Dibujar información
    dibujar_texto(pantalla, f"Nivel: {nivel}", 20, 20)
    dibujar_texto(pantalla, f"Base: {base}", 20, 80)

    # Dibujar letras disponibles
    texto_letras = "Letras: "
    for letra in letras:
        texto_letras = texto_letras + letra + " "
    dibujar_texto(pantalla, texto_letras, 20, 140)

    # Dibujar progreso de la palabra
    dibujar_texto(pantalla, f"Armas: {palabra_actual}", 20, 200)

    pygame.display.update()
    





#Sirve para poner el texto cencentrado en el pygame

def dibujar_texto_centrado(superficie, texto, fuente, color, y):
    surf = fuente.render(texto, True, color)
    x = (superficie.get_width() - surf.get_width()) // 2#ver que significa
    superficie.blit(surf, (x, y))

pygame.quit()