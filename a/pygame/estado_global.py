def crear_estado_global(tiempo_por_nivel):
    estado = {
        "errores_totales": 0,
        "tiempo_restante": float(tiempo_por_nivel)
    }
    return estado