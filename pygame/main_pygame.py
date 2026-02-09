import pygame
from nucleo_pygame import crear_estado_partida
from csv_datos import cargar_niveles
from acciones_jugador import accion_submit, accion_clear, accion_shuffle
from comodines import *
from accesibilidad import obtener_config_visual

pygame.init()
PANTALLA = pygame.display.set_mode((900, 600))
FUENTE = pygame.font.SysFont("arial", 28)
CLOCK = pygame.time.Clock()

def main():
    niveles = cargar_niveles()
    nivel = niveles[0]
    partida = nivel["partidas"][0]

    perfil = "tea"  # viene del login JSON
    estado = crear_estado_partida(partida["letras"], partida["validas"], perfil)
    visual = obtener_config_visual(perfil)

    letras = partida["letras"]

    corriendo = True
    while corriendo:
        CLOCK.tick(60)
        PANTALLA.fill(visual["fondo"])

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    estado = accion_submit(estado)

                if ev.key == pygame.K_BACKSPACE:
                    estado = accion_clear(estado)

                if ev.key == pygame.K_SPACE:
                    letras = accion_shuffle(letras)

        texto = FUENTE.render(
            f"Puntaje: {estado['puntaje']}  Errores: {estado['errores']}",
            True,
            visual["texto"]
        )
        PANTALLA.blit(texto, (20, 20))

        pygame.display.flip()

    pygame.quit()

main()