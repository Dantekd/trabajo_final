
def obtener_config_visual(perfil):
    config = {
        "fondo": (255, 168, 89),
        "texto": (0, 0, 0),
        "animaciones": True
    }

    if perfil == "tea":
        config["fondo"] = (230, 230, 230)
        config["texto"] = (20, 20, 20)
        config["animaciones"] = False

    return config