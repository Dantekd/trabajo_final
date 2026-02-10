import pygame
#Panel de control del audio
def controlar_audio(keys, pantalla, sonido_arriba, sonido_abajo, sonido_mute, sonido_max):
    
    # Bajar volumen
    if keys[pygame.K_0] and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
        pantalla.blit(sonido_abajo, (830, 550))

    elif keys[pygame.K_0] and pygame.mixer.music.get_volume() == 0.0:
        pantalla.blit(sonido_mute, (830, 550))

    # Subir volumen
    if keys[pygame.K_9] and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
        pantalla.blit(sonido_arriba, (830, 550))

    elif keys[pygame.K_9] and pygame.mixer.music.get_volume() == 1.0:
        pantalla.blit(sonido_max, (830, 550))

    # Mute
    if keys[pygame.K_m]:
        pygame.mixer.music.set_volume(0.0)
        pantalla.blit(sonido_mute, (830, 550))

    if keys[pygame.K_COMMA]:
        pygame.mixer.music.set_volume(1.0)
        pantalla.blit(sonido_max, (830, 550))
