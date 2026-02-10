import pygame
import json
from ui_dibujado import *
from ui_botones import *


RUTA_JSON = r"C:/Users/Usuario/Desktop/trabajo_final/Final/pygame/datos.json"


pygame.init()

PANTALLA = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Login Juego")
FUENTE = pygame.font.SysFont("arial", 28)


def cargar_datos_json():
    archivo = open(RUTA_JSON, "r")
    datos = json.load(archivo)
    archivo.close()
    return datos


def guardar_datos_json(datos):
    archivo = open(RUTA_JSON, "w")
    json.dump(datos, archivo, indent=4)
    archivo.close()

# Busca el usuarios dentro de json

def buscar_usuario(datos, nombre, contra):
    indice_encontrado = -1

    for i in range(len(datos["usuarios"])):
        if datos["usuarios"][i]["nombre_usuario"] == nombre and datos["usuarios"][i]["contrasena"] == contra:
            indice_encontrado = i

    return indice_encontrado


#Crea un nuevo usuarios
def crear_usuario(datos, nombre, contra):

    datos["usuarios"].append({
        "nombre_usuario": nombre,
        "contrasena": contra,
        "modo": "normal",
        "accesibilidad": {
            "tdah": False
        },
        "stats": {
            "puntaje_total": 0,
            "errores_totales": 0,
            "partidas_jugadas": 0
        }
    })

    return len(datos["usuarios"]) - 1


# =========================================================
# MANEJAR EVENTOS LOGIN
# =========================================================
def manejar_eventos_login(evento, user_text, pass_text, activo_user, activo_pass):

    if evento.type == pygame.MOUSEBUTTONDOWN:

        if pygame.Rect(300, 200, 300, 40).collidepoint(evento.pos):
            activo_user = True
            activo_pass = False

        elif pygame.Rect(300, 300, 300, 40).collidepoint(evento.pos):
            activo_user = False
            activo_pass = True

    elif evento.type == pygame.KEYDOWN:

        # Backspace elimina el último carácter
        if evento.key == pygame.K_BACKSPACE:
            if activo_user:
                user_text = user_text[:-1]
            elif activo_pass:
                pass_text = pass_text[:-1]

        # Agregar caracteres imprimibles a su campo correspondiente
        elif evento.unicode and evento.key != pygame.K_RETURN:
            if activo_user:
                user_text += evento.unicode
            elif activo_pass:
                pass_text += evento.unicode

        
    return user_text, pass_text, activo_user, activo_pass


# =========================================================
# PANTALLA LOGIN PRINCIPAL
# =========================================================

def pantalla_login():

    datos = cargar_datos_json()
    normalizar_usuarios(datos)
    guardar_datos_json(datos)

    botones = crear_botones_login()

    user_text = ""
    pass_text = ""
    activo_user = True
    activo_pass = False
    usuario_logueado = -1
    mensaje_error = ""

    corriendo = True
    while corriendo:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            user_text, pass_text, activo_user, activo_pass = manejar_eventos_login(evento, user_text, pass_text, activo_user, activo_pass)
            
              # ===== ENTER = SOLO LOGIN =====
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                indice = buscar_usuario(datos, user_text, pass_text)
                if indice != -1:
                    usuario_logueado = indice
                    corriendo = False
                else:
                    mensaje_error = "Usuario o contraseña incorrectos"
            
            
            if evento.type == pygame.MOUSEBUTTONDOWN:  
            
                #Registro
                if botones["registro"]["rect"].collidepoint(evento.pos):
                    if user_text == "" or pass_text == "":
                        mensaje_error = "Campos vacíos"
                    else:
                        nombres = [u["nombre_usuario"] for u in datos["usuarios"]]
                        if user_text in nombres:
                            mensaje_error = "Usuario ya existe"
                        else:
                            usuario_logueado = crear_usuario(datos, user_text, pass_text)
                            guardar_datos_json(datos)
                            corriendo = False

        # Dibujar login y mensaje de error
        dibujar_login(PANTALLA, user_text, pass_text, activo_user, activo_pass)
        dibujar_botones(PANTALLA, botones["registro"], FUENTE)

        if mensaje_error:
            dibujar_texto(PANTALLA, mensaje_error, FUENTE, (255, 0, 0), 300, 370)
    
        pygame.display.update()

    return usuario_logueado

# =========================================================
# MANEJAR EVENTOS CONFIG
# =========================================================
def manejar_eventos_configuracion(evento, config):

    if evento.type == pygame.MOUSEBUTTONDOWN:

        if pygame.Rect(250, 250, 200, 80).collidepoint(evento.pos):
            config = "estandar"

        if pygame.Rect(600, 250, 200, 80).collidepoint(evento.pos):
            config = "daltonico"

    return config


# =========================================================
# PANTALLA CONFIGURACION
# =========================================================
def pantalla_configuracion(indice_usuario):

    datos = cargar_datos_json()
    normalizar_usuarios(datos)
    guardar_datos_json(datos)
    botones = crear_botones_configuracion()

    modo_elegido = datos["usuarios"][indice_usuario]["modo"]
    corriendo = True

    
    while corriendo:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if botones["normal"]["rect"].collidepoint(evento.pos):
                    datos["usuarios"][indice_usuario]["modo"] = "normal"
                    datos["usuarios"][indice_usuario]["accesibilidad"]["tdah"] = False
                    modo_elegido = "normal"
                    corriendo = False

                elif botones["tdah"]["rect"].collidepoint(evento.pos):
                    datos["usuarios"][indice_usuario]["modo"] = "tdah"
                    datos["usuarios"][indice_usuario]["accesibilidad"]["tdah"] = True
                    modo_elegido = "tdah"
                    corriendo = False

        dibujar_configuracion(PANTALLA, FUENTE, botones)
        pygame.display.update()

    guardar_datos_json(datos)
    return modo_elegido
#La u representa a el usuario y la función sirve para asegurar que todos los usuarios tengan la misma estructura
def normalizar_usuarios(datos):
    for u in datos["usuarios"]:

        if "modo" not in u:
            u["modo"] = "normal"

        if "accesibilidad" not in u:
            u["accesibilidad"] = {"tdah": False}

        if "tdah" not in u["accesibilidad"]:
            u["accesibilidad"]["tdah"] = False

        if "stats" not in u:
            u["stats"] = {
                "puntaje_total": 0,
                "errores_totales": 0,
                "partidas_jugadas": 0
            }
def main():

    indice = pantalla_login()
    config = pantalla_configuracion(indice)

    print("Usuario indice:", indice)
    print("Configuracion elegida:", config)

