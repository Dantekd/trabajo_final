import pygame
import json
from ui_dibujado import *
from ui_botones import *

RUTA_JSON = r"C:/Users/Usuario/Desktop/trabajo_final/Final/pygame/datos.json"

pygame.init()

PANTALLA = pygame.display.set_mode((900, 600))

pygame.display.set_caption("Login Juego")
FUENTE = pygame.font.SysFont("arial", 28)

#Carga la información existente en Json
def cargar_datos_json():
    archivo = open(RUTA_JSON, "r")
    datos = json.load(archivo)
    archivo.close()
    return datos

#Guarda los datos obtenidos de Json
def guardar_datos_json(datos):
    archivo = open(RUTA_JSON, "w")
    json.dump(datos, archivo, indent=4)#Desglosa la linea dump
    archivo.close()

# Busca un usuario puntual recorriendo los usuarios dentro de json
def buscar_usuario(datos, nombre, contra):
    indice_encontrado = -1

    for i in range(len(datos["usuarios"])):
        if datos["usuarios"][i]["nombre_usuario"] == nombre and datos["usuarios"][i]["contrasena"] == contra:
            indice_encontrado = i

    return indice_encontrado


#Crea un nuevo usuario y caracteristicas base
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

    return len(datos["usuarios"]) - 1#Devuelve el indice de usuario recien creado


#Controla los sucesos dentro del login
def manejar_eventos_login(evento, user_text, pass_text, activo_user, activo_pass):
    #Cuando el mouse lo clickea
    if evento.type == pygame.MOUSEBUTTONDOWN:
        #Cuadros de diferentes colores segun que caja de texto este activo
        if pygame.Rect(300, 200, 300, 40).collidepoint(evento.pos):
            activo_user = True
            activo_pass = False

        elif pygame.Rect(300, 300, 300, 40).collidepoint(evento.pos):
            activo_user = False
            activo_pass = True
    #cuando se activa KEYdown trae dos cosas
    elif evento.type == pygame.KEYDOWN:

        # Esto permite que lo ingresado se pueda borrar con la tecla de borrar
        #key es la tecla fisica que se se toco
        if evento.key == pygame.K_BACKSPACE:
            if activo_user:
                user_text = user_text[:-1]
            elif activo_pass:
                pass_text = pass_text[:-1]

        # Agregar caracteres imprimibles a su campo correspondiente
        #unicodde seria el caracter 
        elif evento.unicode and evento.key != pygame.K_RETURN:
            if activo_user:
                user_text += evento.unicode
            elif activo_pass:
                pass_text += evento.unicode

        
    return user_text, pass_text, activo_user, activo_pass


#Esto es el front-end del login

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
    #Se activa todo 
    while corriendo:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            user_text, pass_text, activo_user, activo_pass = manejar_eventos_login(evento, user_text, pass_text, activo_user, activo_pass)
            
            #Si toca enter se logea
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                indice = buscar_usuario(datos, user_text, pass_text)
                if indice != -1:
                    usuario_logueado = indice
                    corriendo = False
                else:
                    #Esto pasas si ingresa algo incorrecto
                    mensaje_error = "Usuario o contraseña incorrectos"
            
            #Detecta el click del Mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:  
            
                #Con esto te permite registrarte y lo que puede suceder
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

#Esto son las cosas con las que el usuario puede interactuar en configuración
def manejar_eventos_configuracion(evento, config):

    if evento.type == pygame.MOUSEBUTTONDOWN:

        if pygame.Rect(250, 250, 200, 80).collidepoint(evento.pos):
            config = "normal"

        if pygame.Rect(600, 250, 200, 80).collidepoint(evento.pos):
            config = "tdah"

    return config

#Esto es lo que ve el usuario de configuración
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
            #Al clickear con el Mouse dentro de esa area sucede eso
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