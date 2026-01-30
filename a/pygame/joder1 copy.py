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
from nucleo_pygame import crear_estado_pygame, procesar_palabra_pygame, verificar_fin_pygame
from logicas_pygame import dibujar_vertical_degradado

# ========== INICIALIZACION PYGAME ==========
pygame.init()
DIM = (900, 600)
PANTALLA = pygame.display.set_mode(DIM)
pygame.display.set_caption("AHORCADO  - Encina-Diaz")

# icono (usa RUTA_ACTUAL para evitar rutas absolutas)
try:
    icono_path = os.path.join(RUTA_ACTUAL, "icono_juego.jpg")
    icono = pygame.image.load(icono_path)
    pygame.display.set_icon(icono)
except Exception:
    # si falta, no rompe: seguimos sin icono
    pass

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
    x = (superficie.get_width() - surf.get_width()) // 2#ver que significa
    superficie.blit(surf, (x, y))

def crear_botones_letras_csv(letras):
    botones = []
    x = 100
    y = 420

    for letra in letras:
        rect = pygame.Rect(x, y, 48, 48)
        botones.append({
            "letra": letra.upper(),
            "rect": rect,
            "activa": True
        })
        x += 58

    return botones


def crear_boton_usado(letra, index):
    x = 100 + index * 58
    y = 500
    return {
        "letra": letra,
        "rect": pygame.Rect(x, y, 48, 48)
    }

# ========== LOGICA DE PARTIDA (HÍBRIDA) ==========

 
def ejecutar_partida_pygame(partida: dict) -> int:
    """
    Ejecuta una partida híbrida: revela letras en la palabra objetivo (la más larga),
    y permite ingresar palabras completas para validar/puntuar.
    Devuelve puntaje obtenido en la partida.
    """
    base_set, base_lista, palabras_validas = preparar_partida(partida)

    estado = crear_estado_pygame(base_lista, palabras_validas)

    botones_disponibles = crear_botones_letras_csv(base_lista)
    botones_usados = []
    palabra_actual = []

    tiempo_restante = 60.0
    clock = pygame.time.Clock()
    running = True

    mensaje = ""
    mensaje_timer = 0.0

    palabras_descubiertas = 0

    def mostrar_mensaje(m):
        nonlocal mensaje, mensaje_timer
        mensaje = m
        mensaje_timer = 2.0

    while running:
        dt = clock.tick(60) / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # CLICK EN BOTONES SUPERIORES
                for boton in botones_disponibles:
                    if boton["activa"] and boton["rect"].collidepoint(pos):
                        boton["activa"] = False
                        palabra_actual.append(boton["letra"])
                        botones_usados.append(
                            crear_boton_usado(boton["letra"], len(botones_usados))
                        )

                # CLICK EN BOTONES INFERIORES (DESHACER)
                i = 0
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

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    if len(palabra_actual) > 0:
                        palabra = "".join(palabra_actual)

                        resultado = procesar_palabra_pygame(estado, palabra)

                        if resultado == "valida":
                            mostrar_mensaje("Palabra válida")
                            palabras_descubiertas += 1
                        elif resultado == "repetida":
                            mostrar_mensaje("Palabra repetida")
                        else:
                            mostrar_mensaje("Palabra inválida")

                        palabra_actual.clear()
                        botones_usados.clear()
                        for b in botones_disponibles:
                            b["activa"] = True

        tiempo_restante -= dt
        if tiempo_restante <= 0:
            mostrar_mensaje("Se acabó el tiempo")
            running = False

        if estado["errores"] >= estado["intentos_maximos"]:
            mostrar_mensaje("Máximos errores alcanzados")
            running = False

        if len(estado["palabras_encontradas"]) >= len(estado["palabras_validas"]):
            mostrar_mensaje("No quedan palabras")
            running = False

        # ===== DIBUJADO =====
        dibujar_vertical_degradado(PANTALLA, (10, 10, 60), (10, 120, 200))

        # BOTONES SUPERIORES
        for boton in botones_disponibles:
            color = (120, 120, 255) if boton["activa"] else (70, 70, 70)
            pygame.draw.circle(PANTALLA, color, boton["rect"].center, 22)
            letra = FUENTE_PEQ.render(boton["letra"], True, (0, 0, 0))
            PANTALLA.blit(letra, (boton["rect"].x + 14, boton["rect"].y + 10))

        # BOTONES INFERIORES
        for boton in botones_usados:
            pygame.draw.circle(PANTALLA, (255, 200, 100), boton["rect"].center, 22)
            letra = FUENTE_PEQ.render(boton["letra"], True, (0, 0, 0))
            PANTALLA.blit(letra, (boton["rect"].x + 14, boton["rect"].y + 10))

        # TIEMPO
        PANTALLA.blit(
            FUENTE_TIMER.render(f"Tiempo: {int(tiempo_restante)}", True, (255, 255, 255)),
            (740, 20)
        )

        # CONTADOR PALABRAS
        PANTALLA.blit(
            FUENTE_PEQ.render(
                f"Palabras: {len(estado['palabras_encontradas'])}/{len(estado['palabras_validas'])}",
                True,
                (255, 255, 255)
            ),
            (20, 20)
        )

        if mensaje_timer > 0:
            PANTALLA.blit(
                FUENTE_PEQ.render(mensaje, True, (255, 255, 0)),
                (50, 300)
            )
            mensaje_timer -= dt

        pygame.display.update()

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
