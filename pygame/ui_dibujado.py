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

def dibujar_texto_centrado(pantalla,texto,fuente,color,y):
    """
    Dibuja un texto centrado horizontalmente en la pantalla.
    """
    superficie = fuente.render(texto, True, color)
    x = (pantalla.get_width() - superficie.get_width()) // 2
    pantalla.blit(superficie, (x, y))
    
def dibujar_rect_redondeado(superficie,color,x, y,ancho, alto,radio=None,borde=0):
    """
    Dibuja un rectángulo con bordes redondeados.
    
    radio: si es None, se usa alto // 2 (tipo cápsula)
    borde: 0 = relleno, >0 = solo borde
    """
    if radio is None:
        radio = alto // 2

    pygame.draw.rect(superficie,color,(x, y, ancho, alto),borde,border_radius=radio)

def dibujar_juego(pantalla,estado,botones_disponibles,botones_usados,fuente_pequena,fuente_timer,tiempo_restante,mensaje,mensaje_timer,dt):

    dibujar_vertical_degradado(pantalla, (238,118,94), (255,168,89))
    dibujar_rect_redondeado(pantalla,(250,155,155),100,310,670,60,borde=0)

    dibujar_botones_disponibles(pantalla, botones_disponibles, fuente_pequena)
    dibujar_botones_usados(pantalla, botones_usados, fuente_pequena)

    pantalla.blit(
        fuente_timer.render(f"Tiempo: {int(tiempo_restante)}", True, (255,255,255)),
        (740,20)
    )

    pantalla.blit(
        fuente_pequena.render("Errores: " + str(estado["errores"]), True, (255,180,180)),
        (20,52)
    )

    pantalla.blit(
        fuente_pequena.render(
            f"Palabras: {len(estado['palabras_encontradas'])}/{len(estado['palabras_validas'])}",
            True,
            (255,255,255)
        ),
        (20,20)
    )

    if mensaje_timer > 0:
        pantalla.blit(
            fuente_pequena.render(mensaje, True, (255,255,0)),
            (340,25)
        )
        mensaje_timer -= dt

    return mensaje_timer
#Esto va a aparecer cuando se clickean los comodines
def dibujar_comodines(pantalla, botones, comodines_nivel, fuente):

    colores = {
        "tiempo": (100, 200, 255),
        "errores": (255, 120, 120),
        "nivel": (200, 120, 255)
    }

    textos = {
        "tiempo": "+30s",
        "errores": "Reset",
        "nivel": "50/50"
    }

    for b in botones:
        usado = comodines_nivel[b["tipo"]]
        color = (70, 70, 70) if usado else colores[b["tipo"]]

        pygame.draw.rect(pantalla, color, b["rect"], border_radius=12)

        txt = fuente.render(textos[b["tipo"]], True, (0,0,0))
        pantalla.blit(txt, txt.get_rect(center=b["rect"].center))

#degradado de fondo
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




