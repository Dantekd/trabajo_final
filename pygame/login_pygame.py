# =========================================================
# LOGIN + CONFIGURACION EN PYGAME (MODULARIZADO)
# SIN TRY/EXCEPT
# UN SOLO RETURN POR FUNCION
# TODO COMENTADO
# =========================================================

import pygame
import json
from ui_dibujado import *

# =========================================================
# RUTA JSON (USA TU RUTA REAL)
# =========================================================
RUTA_JSON = r"C:/Users/Usuario/Desktop/trabajo_final/Final/pygame/datos.json"

# =========================================================
# INICIALIZAR PYGAME
# =========================================================
pygame.init()
pygame.init()
PANTALLA = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Login Juego")
FUENTE = pygame.font.SysFont("arial", 28)

# =========================================================
# FUNCION: CARGAR JSON
# =========================================================
def cargar_datos_json():
    archivo = open(RUTA_JSON, "r")
    datos = json.load(archivo)
    archivo.close()
    return datos


# =========================================================
# FUNCION: GUARDAR JSON
# =========================================================
def guardar_datos_json(datos):
    archivo = open(RUTA_JSON, "w")
    json.dump(datos, archivo, indent=4)
    archivo.close()

# =========================================================
# FUNCION: BUSCAR USUARIO EXISTENTE
# =========================================================
def buscar_usuario(datos, nombre, contra):
    indice_encontrado = -1

    for i in range(len(datos["usuario"])):
        if datos["usuario"][i]["nombre_usuario"] == nombre and datos["usuario"][i]["contrasena"] == contra:
            indice_encontrado = i

    return indice_encontrado


# =========================================================
# FUNCION: CREAR NUEVO USUARIO
# =========================================================
def crear_usuario(datos, nombre, contra):

    datos["usuario"].append({
        "nombre_usuario": nombre,
        "contrasena": contra
    })

    datos["stats"].append({
        "puntaje": 0,
        "partidas_guardadas": 0,
        "configuracion": "estandar",
        "errores": 0
    })
    #fijarte como reemplazarlo
    return len(datos["usuario"]) - 1


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
            
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:

                if user_text.strip() == "" or pass_text.strip() == "":
                    mensaje_error = "Usuario y contraseña no pueden estar vacíos."
                else:
                    indice = buscar_usuario(datos, user_text, pass_text)
                    if indice != -1:
                        # Usuario existe y contraseña correcta
                        usuario_logueado = indice
                        corriendo = False
                    else:
                        # Verificar si el usuario ya existe por nombre (evitar duplicados)
                        nombres_existentes = [u["nombre_usuario"] for u in datos["usuario"]]
                        if user_text in nombres_existentes:
                            mensaje_error = "Usuario ya existe, contraseña incorrecta."
                        else:
                            # Crear nuevo usuario
                            nuevo = crear_usuario(datos, user_text, pass_text)
                            guardar_datos_json(datos)
                            usuario_logueado = nuevo
                            corriendo = False

        # Dibujar login y mensaje de error
        dibujar_login(PANTALLA, user_text, pass_text, activo_user, activo_pass)
        if mensaje_error:
            dibujar_texto(PANTALLA, mensaje_error, FUENTE, (255, 0, 0), 300, 370)

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
    for stat in datos["stats"]:
        if "configuracion" not in stat:
            stat["configuracion"] = "estandar"

    config = datos["stats"][indice_usuario]["configuracion"]

    corriendo = True

    while corriendo:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            config = manejar_eventos_configuracion(evento, config)

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                corriendo = False

        dibujar_configuracion(PANTALLA)

    datos["stats"][indice_usuario]["configuracion"] = config
    guardar_datos_json(datos)

    return config


# =========================================================
# MAIN DEMO
# =========================================================

def main():

    indice = pantalla_login()
    config = pantalla_configuracion(indice)

    print("Usuario indice:", indice)
    print("Configuracion elegida:", config)

