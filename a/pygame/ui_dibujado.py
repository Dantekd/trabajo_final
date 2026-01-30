import pygame

def dibujar_botones_disponibles(pantalla, botones, fuente):
    for b in botones:
        color = (120, 120, 255) if b["activa"] else (70, 70, 70)
        pygame.draw.circle(pantalla, color, b["rect"].center, 22)
        txt = fuente.render(b["letra"], True, (0, 0, 0))
        pantalla.blit(txt, (b["rect"].x + 14, b["rect"].y + 10))


def dibujar_botones_usados(pantalla, botones, fuente):
    for b in botones:
        pygame.draw.circle(pantalla, (255, 200, 100), b["rect"].center, 22)
        txt = fuente.render(b["letra"], True, (0, 0, 0))
        pantalla.blit(txt, (b["rect"].x + 14, b["rect"].y + 10))
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
def dibujar_texto_centrado(
    pantalla,
    texto,
    fuente,
    color,
    y
):
    """
    Dibuja un texto centrado horizontalmente en la pantalla.
    """
    superficie = fuente.render(texto, True, color)
    x = (pantalla.get_width() - superficie.get_width()) // 2
    pantalla.blit(superficie, (x, y))
    
def dibujar_rect_redondeado(
    superficie,
    color,
    x, y,
    ancho, alto,
    radio=None,
    borde=0
):
    """
    Dibuja un rectángulo con bordes redondeados.
    
    radio: si es None, se usa alto // 2 (tipo cápsula)
    borde: 0 = relleno, >0 = solo borde
    """
    if radio is None:
        radio = alto // 2

    pygame.draw.rect(
        superficie,
        color,
        (x, y, ancho, alto),
        borde,
        border_radius=radio
    )