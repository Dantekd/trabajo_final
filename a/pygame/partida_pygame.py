import pygame
from logicas_pygame import dibujar_vertical_degradado
import random
from csv_datos import cargar_niveles
from nucleo_juego import jugar_nivel

DIMENSIONES_PANTALLA=(800,500)

PANTALLA=pygame.display.set_mode(DIMENSIONES_PANTALLA)

pygame.display.set_caption("AHORCADO Encina-Diaz")

icono=pygame.image.load("a\icono_juego.jpg")

pygame.display.set_icon(icono)

niveles=cargar_niveles()
nivel_actual=niveles[0]
partida = random.choice(nivel_actual["partidas"])



palabra_actual = ""
encontradas = []

bandera_pantalla= True

# Load words

with open('a\partidas.csv', 'r') as file:
    words = [line.strip().upper() for line in file]

def crear_botones(letras):
    botones = []
    x = 50
    for letra in letras:
        rect = pygame.Rect(x, 400, 40, 40)
        botones.append((letra, rect))
        x += 50
    return botones

botones = crear_botones(base_lista)
clock = pygame.time.Clock()

while bandera_pantalla:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bandera_pantalla=False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for letra, rect in botones:
                if rect.collidepoint(pos):
                    palabra_actual += letra.upper()



      # mostrar palabra actual
    txt2 = font.render(palabra_actual, True, (255,255,0))
    pantalla.blit(txt2,(200,200))


    dibujar_vertical_degradado(PANTALLA, (0, 0, 80), (0, 150, 255))
    pygame.display.flip()
    clock.tick(10) 
pygame.quit()