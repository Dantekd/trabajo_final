import pygame

pygame.font.init()
PANTALLA = pygame.display.set_mode((900, 600))
FUENTE = pygame.font.SysFont("arial", 32)
FUENTE_GRANDE = pygame.font.SysFont("arial", 48)
FUENTE_PEQUENA = pygame.font.SysFont(None, 32)


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
    if estado["mensaje_timer"] > 0:
        dibujar_texto_centrado(PANTALLA,estado["mensaje"],FUENTE_PEQUENA,(255, 255, 0),180)
        estado["mensaje_timer"] -= dt

    if mensaje_timer > 0:
        pantalla.blit(
            fuente_pequena.render(mensaje, True, (255,255,0)),
            (340,25)
        )
        mensaje_timer -= dt
    
    if "mensaje" in estado:
        dibujar_texto (pantalla,estado["mensaje"],fuente_pequena,(255, 255, 0),200,360)

    return mensaje_timer
#Esto va a aparecer cuando se clickean los comodines
def dibujar_comodines(pantalla, botones, comodines_nivel, fuente):

    colores = {
        "revelar": (100, 200, 255),
        "ubicar": (255, 120, 120),
        "nivel": (200, 120, 255)
    }

    textos = {
        "revelar": "Revelar palabra",
        "ubicar": "Ubicar letra",
        "nivel": "50/50"
    }
#b es un diccionario que representa un botón de comodín.
#Esto sirve para que ponga el color correspondiente segun el tipo de comodin.
    for b in botones:
        usado = comodines_nivel[b["tipo"]]
        if usado:
            color = (70, 70, 70)
        else:
            color = colores[b["tipo"]]

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

#Se usa en la demo para mostrar las palabras que se usan durante la partida
def dibujar_palabras_objetivo(pantalla, palabras, fuente):

    y = 120

    titulo = fuente.render("Palabras objetivo:", True, (255,255,0))
    pantalla.blit(titulo, (650, 80))

    for palabra in palabras:
        txt = fuente.render(palabra, True, (255,255,255))
        pantalla.blit(txt, (650, y))
        y += 28


#Con esto se hace lo estetico del login




# =========================================================
# DIBUJAR CONFIGURACION
# =========================================================
def dibujar_configuracion(pantalla):

    pantalla.fill((200, 200, 255))

    # Título centrado
    dibujar_texto(pantalla, "CONFIGURACIÓN ", FUENTE_GRANDE, (0, 0, 0),260, 80)

    # Botones
    pygame.draw.rect(pantalla, (0, 200, 0), (250, 250, 200, 80))
    pygame.draw.rect(pantalla, (200, 0, 0), (500, 250, 200, 80))

    # Texto dentro de botones
    dibujar_texto(pantalla, "ESTANDAR", FUENTE, (0,0,0),260,280)
    dibujar_texto(pantalla, "DALTONICO", FUENTE, (0,0,0),510,280)

    dibujar_texto(pantalla, "VOLUMEN", FUENTE_GRANDE, (0, 0, 0),360, 400)

    dibujar_texto(pantalla, "Mute: m ", FUENTE, (0,0,0),100,520)

    dibujar_texto(pantalla, "Subir: 0 ", FUENTE, (0,0,0),300,520)

    dibujar_texto(pantalla, "Bajar: 9 ", FUENTE, (0,0,0),500,520)

    dibujar_texto(pantalla, "MAX: , ", FUENTE, (0,0,0),700,520)


    pygame.display.flip()


def dibujar_texto(pantalla, texto, fuente, color, x, y):
    """
    Dibuja un texto en la pantalla en la posición (x, y)
    """
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))



def dibujar_login(pantalla,user_text, pass_text, activo_user, activo_pass):

    pantalla.fill((230, 230, 230))

    dibujar_texto_centrado(pantalla,"LOGIN",FUENTE,(0, 0, 0),60)

    color_user = (0, 200, 0) if activo_user else (0, 0, 0)
    color_pass = (0, 200, 0) if activo_pass else (0, 0, 0)

    pygame.draw.rect(pantalla, color_user, (300, 200, 300, 40), 2)
    pygame.draw.rect(pantalla, color_pass, (300, 300, 300, 40), 2)
    dibujar_texto(pantalla, "Usuario:", FUENTE, (0,0,0), 200, 205)
    dibujar_texto(pantalla, "Password:", FUENTE, (0,0,0),170, 305)
    dibujar_texto(pantalla, user_text, FUENTE, (0,0,0), 300, 205)  # ajustar Y si querés
    dibujar_texto(pantalla, "*" * len(pass_text), FUENTE, (0,0,0), 305, 305)  # ajustar Y si querés
    dibujar_texto( pantalla,"ENTER = Ingresar / Crear",FUENTE,(80, 80, 80),305,450)

    pygame.display.flip()

def dibujar_botones_accion(pantalla, botones, fuente):
    for b in botones:
        pygame.draw.rect(pantalla, (80, 80, 80), b["rect"])
        texto = fuente.render(b["texto"], True, (255, 255, 255))
        pantalla.blit(texto, b["rect"].move(10, 5))