import sys
import os
import random
import pygame
import time

# ========== RUTAS ==========
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))     # /a/pygame
RUTA_PROYECTO = os.path.dirname(RUTA_ACTUAL)                 # /a

if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

# ========== IMPORTS DEL PROYECTO ==========
from csv_datos import cargar_niveles
from nucleo_juego import preparar_partida, buscar_partida_aleatoria_sin_repetir
from mecanicas import generar_guiones
from a.pygame.nucleo_pygame import crear_estado_pygame, procesar_palabra_pygame, verificar_fin_pygame
from logicas_pygame import dibujar_vertical_degradado

# ========== INICIALIZACION PYGAME ==========
pygame.init()
DIM = (900, 600)
PANTALLA = pygame.display.set_mode(DIM)
pygame.display.set_caption("AHORCADO  - Encina-Diaz")

# icono (usa RUTA_ACTUAL para evitar rutas absolutas)
icono_path = os.path.join(RUTA_ACTUAL, "icono_juego.jpg")
icono = pygame.image.load(icono_path)
pygame.display.set_icon(icono)


FUENTE = pygame.font.SysFont(None, 48)
FUENTE_PEQ = pygame.font.SysFont(None, 32)
FUENTE_TIMER = pygame.font.SysFont(None, 28)
R_CLOCK = pygame.time.Clock()

# ========== UTILIDADES ==========
def obtener_palabra_mas_larga(palabras: list) -> str:
    """Devuelve la palabra más larga de la lista (si empatan, la primera)."""
    mayor = ""
    i = 0
    while i < len(palabras):
        if len(palabras[i]) > len(mayor):
            mayor = palabras[i]
        i += 1
    return mayor

def crear_botones(letras):
    botones = []
    x = 60
    i = 0
    while i < len(letras):
        rect = pygame.Rect(x, 480, 48, 48)
        botones.append((letras[i], rect))
        x += 58
        i += 1
    return botones

def dibujar_texto_centrado(superficie, texto, fuente, color, y):
    surf = fuente.render(texto, True, color)
    x = (superficie.get_width() - surf.get_width()) // 2
    superficie.blit(surf, (x, y))


# ========== LOGICA DE PARTIDA (HÍBRIDA) ==========
def ejecutar_partida_pygame(partida: dict) -> int:
    """
    Ejecuta una partida híbrida: revela letras en la palabra objetivo (la más larga),
    y permite ingresar palabras completas para validar/puntuar.
    Devuelve puntaje obtenido en la partida.
    """
    # preparar estructura de la partida
    base_set, base_lista, palabras_validas = preparar_partida(partida)
    objetivo = obtener_palabra_mas_larga(palabras_validas)   # palabra a adivinar con guiones
    objetivo_upper = objetivo.upper()

    # guiones como lista mutable
    guiones_list = []
    j = 0
    while j < len(objetivo_upper):
        if objetivo_upper[j].isalpha():
            guiones_list.append("_")
        else:
            guiones_list.append(objetivo_upper[j])
        j += 1

    # estado compartido con nucleo_pygame
    estado = crear_estado_pygame(base_lista, palabras_validas)

    # botones con letras mezcladas
    letras_mez = base_lista[:]
    random.shuffle(letras_mez)
    botones = crear_botones(letras_mez)

    palabra_actual = ""
    tiempo_restante = 60.0
    clock = pygame.time.Clock()
    running = True

    # para indicar resultados temporales en pantalla
    mensaje = ""
    mensaje_timer = 0.0

    def mostrar_mensaje(m):
        nonlocal mensaje, mensaje_timer
        mensaje = m
        mensaje_timer = 2.0  # segundos

    # helper para revelar letras en guiones
    def revelar_letra(letra):
        nonlocal guiones_list
        encontrada = False
        i = 0
        while i < len(objetivo_upper):
            if objetivo_upper[i] == letra:
                guiones_list[i] = letra
                encontrada = True
            i += 1
        return encontrada

    # helper para comprobar si palabra objetivo está completa
    def objetivo_completo():
        i = 0
        completo = True
        while i < len(guiones_list):
            if guiones_list[i] == "_":
                completo = False
                break
            i += 1
        return completo

    # MAIN LOOP de la partida
    while running:
        dt = clock.tick(60) / 1000.0
        # eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ---------- CLIC SOBRE BOTONES ----------
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                i = 0
                while i < len(botones):
                    letra, rect = botones[i]
                    if rect.collidepoint(pos):
                        l = letra.upper()
                        if revelar_letra(l):
                            mostrar_mensaje(f"Letra {l} encontrada")
                        else:
                            estado["errores"] += 1
                            mostrar_mensaje(f"Letra {l} incorrecta")
                    i += 1

            # ---------- TECLADO ----------
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    if len(palabra_actual) > 0:
                        resultado = procesar_palabra_pygame(estado, palabra_actual)

                        if resultado == "valida":
                            mostrar_mensaje("Palabra válida")

                            # solo si la palabra válida es la objetivo la revelamos completa
                            if palabra_actual.lower() == objetivo.lower():
                                k = 0
                                while k < len(objetivo_upper):
                                    guiones_list[k] = objetivo_upper[k]
                                    k += 1

                        elif resultado == "repetida":
                            mostrar_mensaje("Palabra repetida")
                        else:
                            mostrar_mensaje("Palabra inválida")

                        palabra_actual = ""

                elif ev.key == pygame.K_BACKSPACE:
                    if len(palabra_actual) > 0:
                        palabra_actual = palabra_actual[:-1]

                else:
                    if ev.unicode is not None and len(ev.unicode) == 1:
                        c = ev.unicode.upper()
                        if c.isalpha():
                            palabra_actual = palabra_actual + c


        # timer
        tiempo_restante -= dt
        if tiempo_restante <= 0:
            mostrar_mensaje("Se acabó el tiempo")
            running = False

        # comprobar errores maximos (intentos_maximos en estado)
        if estado.get("errores", 0) >= estado.get("intentos_maximos", 5):
            mostrar_mensaje("Máximos errores alcanzados")
            running = False

        # comprobar objetivo completado
      # comprobar objetivo completado
        if objetivo_completo():
            mostrar_mensaje("¡Palabra encontrada!")
            palabra_minus = objetivo.lower()
            existe = False
            ii = 0
            while ii < len(estado["palabras_encontradas"]):
                if estado["palabras_encontradas"][ii] == palabra_minus:
                    existe = True
                ii += 1
            if not existe:
                estado["palabras_encontradas"].append(palabra_minus)
            # NO salimos aún: sigue la partida si quedan más palabras
            # running = False   <-- ESTA LÍNEA SE QUITA
        

        # ---- comprobar si ya no quedan palabras ----
            total = len(estado["palabras_validas"])
            encontradas = len(estado["palabras_encontradas"])

            if encontradas >= total:
                mostrar_mensaje("¡No quedan palabras por descubrir!")
                running = False

        # dibujado
        dibujar_vertical_degradado(PANTALLA, (10, 10, 60), (10, 120, 200))

        # mostrar guiones (convertir lista a string con espacios)
        s = ""
        kk = 0
        while kk < len(guiones_list):
            s += guiones_list[kk] + " "
            kk += 1
        txt = FUENTE.render(s.strip(), True, (255, 255, 255))
        PANTALLA.blit(txt, (50, 140))

        # palabra actual (lo que el jugador arma)
        txt2 = FUENTE.render(palabra_actual, True, (255, 255, 0))
        PANTALLA.blit(txt2, (50, 220))

        # botones
        i = 0
        while i < len(botones):
            letra, rect = botones[i]
            pygame.draw.circle(PANTALLA, (120, 120, 255), rect.center, 22)
            L = FUENTE_PEQ.render(letra.upper(), True, (0, 0, 0))
            PANTALLA.blit(L, (rect.x + 12, rect.y + 8))
            i += 1

        # puntaje / errores / tiempo
        PANTALLA.blit(FUENTE_PEQ.render("Puntaje: " + str(estado["puntaje"]), True, (255, 255, 255)), (20, 20))
        PANTALLA.blit(FUENTE_PEQ.render("Errores: " + str(estado["errores"]), True, (255, 180, 180)), (20, 52))
        PANTALLA.blit(FUENTE_TIMER.render("Tiempo: " + str(int(tiempo_restante)), True, (255, 255, 255)), (740, 20))

        # mensaje temporal
        if mensaje_timer > 0:
            PANTALLA.blit(FUENTE_PEQ.render(mensaje, True, (255, 255, 0)), (50, 300))
            mensaje_timer -= dt

        pygame.display.update()

    # fin de la partida: devolvemos puntaje actual
    return estado["puntaje"]


# ========== FLUJO DE NIVELES Y PARTIDAS ==========
def jugar_toda_la_demo(max_niveles: int = 5, max_partidas_por_nivel: int = 3):
    niveles = cargar_niveles()
    puntaje_total = 0
    i_nivel = 0
    # limitar a lo disponible y a max_niveles
    limite_niveles = len(niveles)
    if limite_niveles > max_niveles:
        limite_niveles = max_niveles

    while i_nivel < limite_niveles:
        nivel = niveles[i_nivel]
        partidas_jugadas = 0
        # jugar hasta max_partidas_por_nivel o hasta agotar partidas
        while partidas_jugadas < max_partidas_por_nivel and partidas_jugadas < len(nivel["partidas"]):
            # obtener partida aleatoria sin repetir
            datos = buscar_partida_aleatoria_sin_repetir(nivel)
            puntos = ejecutar_partida_pygame(datos)

            # mostrar pantalla de resumen y esperar tecla para continuar
            mostrar_resumen_partida(puntos)
            puntaje_total += puntos

            partidas_jugadas += 1

        i_nivel += 1

    # FIN DEMO: mostrar puntaje total
    mostrar_resumen_final(puntaje_total)


def mostrar_resumen_partida(puntos_obtenidos: int):
    # pinta una pantalla simple con el puntaje de la partida y espera tecla para seguir
    espera = True
    while espera:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                espera = False

        dibujar_vertical_degradado(PANTALLA, (0, 0, 80), (0, 150, 255))
        dibujar_texto_centrado(PANTALLA, f"Puntos esta partida: {puntos_obtenidos}", FUENTE, (255, 255, 255), 200)
        dibujar_texto_centrado(PANTALLA, "Presiona cualquier tecla para continuar...", FUENTE_PEQ, (200, 200, 200), 260)
        pygame.display.update()
        R_CLOCK.tick(30)


def mostrar_resumen_final(total):
    espera = True
    while espera:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                espera = False

        dibujar_vertical_degradado(PANTALLA, (5, 20, 50), (0, 100, 180))
        dibujar_texto_centrado(PANTALLA, f"Puntaje total: {total}", FUENTE, (255, 255, 255), 200)
        dibujar_texto_centrado(PANTALLA, "Demo finalizada. Presiona cualquier tecla para salir.", FUENTE_PEQ, (200, 200, 200), 260)
        pygame.display.update()
        R_CLOCK.tick(30)


# ========== START ==========
if __name__ == "__main__":
    jugar_toda_la_demo(max_niveles=5, max_partidas_por_nivel=3)
    pygame.quit()
