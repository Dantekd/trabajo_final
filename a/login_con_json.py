# MODULO PARA EL LOGIN DEFINITIVO???

import json

def cargar_datos():
    #with open("datos.json", "r") as f:
    #    return json.load(f)
    with open(r"C:\Users\Usuario\Desktop\Segundo_parcial\a\datos.json", "r") as f:
        return json.load(f)

datos = cargar_datos()
usuario = datos["usuario"]
stats = datos["stats"] 

##################################################################


def guardar_datos(usuario, stats):
    datos = {"usuario": usuario, "stats": stats}
    with open(r"C:\Users\Usuario\Desktop\Segundo_parcial\a\datos.json", "w") as f:
        json.dump(datos, f, indent=4)


###################################################################
def inicio_sesion(usuario, stats):
    registro_usuario = input("Ingrese su nombre de usuario (Enter si no tiene): ")

    # Si tiene un usuario y contraseña previas:
    if registro_usuario != "":
        registro_contraseña = input("Ingrese su contraseña: ")
        encontrado = False

        for i in range(len(usuario)):
            if usuario[i]["nombre_usuario"] == registro_usuario and usuario[i]["contraseña"] == registro_contraseña:
                print(f"Bienvenido {registro_usuario}")
                print(f"Las estadísticas son: {stats[i]['puntaje']}")
                print(f"Partidas guardadas: {stats[i]['partidas_guardadas']}")
                print(f"Configuración: {stats[i]['configuración']}")
                print(f"Errores: {stats[i]['errores']}")
                encontrado = True
                break

        if not encontrado:
            print("Usuario o contraseña incorrectos.")
#te aparece esto si no tenias cuenta previa

    else:
        nuevo_usuario = input("Ingrese un nombre para crear su usuario: ")
        nueva_contraseña = input("Ingrese alguna contraseña: ")

        usuario.append({"nombre_usuario": nuevo_usuario, "contraseña": nueva_contraseña})
        stats.append({"puntaje": 0, "partida_guardadas": 0, "configuración": "estandar", "errores":0})

        print("Usuario creado correctamente.")

datos = cargar_datos()
usuario = datos["usuario"]
stats = datos["stats"]

inicio_sesion(usuario, stats)

guardar_datos(usuario, stats)