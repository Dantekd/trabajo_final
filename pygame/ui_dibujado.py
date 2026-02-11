import pygame
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 32)
FUENTE_GRANDE = pygame.font.SysFont("arial", 45)
FUENTE_PEQUENA = pygame.font.SysFont(None, 25)
FUENTE_TITULO=pygame.font.SysFont("Old English Text",90)
#Dibuja los botones con las letras sacados del csv
def dibujar_botones_disponibles(pantalla, botones, fuente):
    for b in botones:
        #Si esta activa tiene un color y sino esta activa tiene otro color
        if b["activa"]:
            color = (120, 120, 255)
        else:
            color = (70, 70, 70)

        pygame.draw.circle(pantalla, color, b["rect"].center, 22)
        txt = fuente.render(b["letra"], True, (0, 0, 0))
        pantalla.blit(txt, (b["rect"].x + 14, b["rect"].y + 10))
#Proceso similar a la función de botones dispobles
def dibujar_botones_usados(pantalla, botones, fuente):
    for b in botones:
        pygame.draw.circle(pantalla, (255, 200, 100), b["rect"].center, 22)
        txt = fuente.render(b["letra"], True, (0, 0, 0))
        pantalla.blit(txt, (b["rect"].x + 14, b["rect"].y + 10))
#Esto es lo que hace el degradado de fondo del juego
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
#Dibuja el texto siempre en mitad de la pantalla
def dibujar_texto_centrado(pantalla,texto,fuente,color,y):
  
    superficie = fuente.render(texto, True, color)
    x = (pantalla.get_width() - superficie.get_width()) // 2
    pantalla.blit(superficie, (x, y))
    
#Esto es lo que hace el rectángulo con bordes redondeados que tienen adentro los botones usados
def dibujar_rect_redondeado(superficie,color,x, y,ancho, alto,radio=None,borde=0):
    if radio is None:
        radio = alto // 2

    pygame.draw.rect(superficie,color,(x, y, ancho, alto),borde,border_radius=radio)

#Dibuja el front-end principal del juego 
def dibujar_juego(pantalla,estado,botones_disponibles,botones_usados,fuente_pequena,fuente_timer,tiempo_restante,mensaje,mensaje_timer,dt):

    dibujar_vertical_degradado(pantalla, (238,118,94), (255,168,89))
    dibujar_rect_redondeado(pantalla,(250,155,155),100,310,670,60,borde=0)

    dibujar_botones_disponibles(pantalla, botones_disponibles, fuente_pequena)
    dibujar_botones_usados(pantalla, botones_usados, fuente_pequena)
    if estado["tdah"]:
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
    pantalla.blit(
    fuente_pequena.render(
        f"Nivel: {estado['nivel_actual']}  |  Partida: {estado['partida_actual']}",
        True,
        (255,255,255)
    ),
    (680, 60)
    )
    # Mensaje al usar un comodin
    if estado.get("mensaje_comodin_timer", 0) > 0:
        dibujar_texto_centrado(pantalla,estado["mensaje_comodin"],FUENTE_PEQUENA,(255, 255, 0),170)
        estado["mensaje_comodin_timer"] -= dt

    # Mensaje de las palabras cuando ingresas algo
    elif estado.get("mensaje_timer", 0) > 0:
        dibujar_texto_centrado(pantalla,estado["mensaje"],FUENTE_PEQUENA,(255, 255, 255),200)
        estado["mensaje_timer"] -= dt
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


#Dibuja toda la pantalla de configuración osea donde esta el titulo, eleccion de modo y demas.
def dibujar_configuracion(pantalla,FUENTE,botones):

    pantalla.fill((250,250,250))

    # Título centrado
    dibujar_texto(pantalla, "Descubre la palabra ", FUENTE_TITULO, (0, 0, 0),100, 70)
    dibujar_texto(pantalla, "MODO:", FUENTE_GRANDE, (0, 0, 0),50, 270)

    # Botones
    for b in botones.values():
        pygame.draw.rect(pantalla, (0, 0, 0), b["rect"], border_radius=12)
        texto = FUENTE.render(b["texto"], True, (255, 255, 255))
        pantalla.blit(texto, texto.get_rect(center=b["rect"].center))

    dibujar_texto(pantalla, "Controles del Volumen", FUENTE_GRANDE, (0, 0, 0),220, 440)

    dibujar_texto(pantalla, "Mute: m ", FUENTE, (224,168,1),100,520)

    dibujar_texto(pantalla, "Subir: 9 ", FUENTE, (224,168,1),300,520)

    dibujar_texto(pantalla, "Bajar: 0 ", FUENTE, (224,168,1),500,520)

    dibujar_texto(pantalla, "Maximo: , ", FUENTE, (224,168,1),700,520)

#Sirve para poner texto fijo 
def dibujar_texto(pantalla, texto, fuente, color, x, y):
    """
    Dibuja un texto en la pantalla en la posición (x, y)
    """
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))


#Dibuja todo lo visual de la pantalla de login 
def dibujar_login(pantalla,user_text, pass_text, activo_user, activo_pass):

    pantalla.fill((230, 230, 230))

    dibujar_texto_centrado(pantalla,"LOGIN",FUENTE,(0, 0, 0),60)

    color_user = (0, 200, 0) if activo_user else (0, 0, 0)
    color_pass = (0, 200, 0) if activo_pass else (0, 0, 0)

    pygame.draw.rect(pantalla, color_user, (300, 200, 300, 40), 2)
    pygame.draw.rect(pantalla, color_pass, (300, 300, 300, 40), 2)
    dibujar_texto(pantalla, "Usuario:", FUENTE, (0,0,0), 200, 200)
    dibujar_texto(pantalla, "Password:", FUENTE, (0,0,0),170, 305)
    dibujar_texto(pantalla, user_text, FUENTE, (0,0,0), 300, 205)  # ajustar Y si querés
    dibujar_texto(pantalla, "*" * len(pass_text), FUENTE, (0,0,0), 305, 305)  # ajustar Y si querés
    dibujar_texto( pantalla,"Ingrese Enter si quiere loguearse. ",FUENTE_PEQUENA,(80, 80, 80),320,500)
    dibujar_texto( pantalla,"Si quiere registrarse porfavor complete los campos con lo deseado y toque el boton.",FUENTE_PEQUENA,(80, 80, 80),100,550)

#esto es algo mas puntual que se usa en acciones_jugador
def dibujar_botones_accion(pantalla, botones, fuente):
    for b in botones:
        dibujar_botones(pantalla, b, fuente)
#Esto es una funcion mas generica que se usa en login
def dibujar_botones(pantalla, boton, fuente):
    pygame.draw.rect(pantalla, (80,80,80), boton["rect"])
    texto = fuente.render(boton["texto"], True, (255,255,255))
    pantalla.blit(texto, boton["rect"].move(10, 10))