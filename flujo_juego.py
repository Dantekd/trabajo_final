# MODULO QUE CONTROLA EL FLUJO DEL JUEGO.
from nucleo_juego import buscar_partida_aleatoria_sin_repetir
from nucleo_juego_solo_consola import jugar_partida
from mecanicas import ordenar_minimo
from auxiliares_flujo_juego import *
from auxiliares_comodines import procesar_resultado_partida



###################################################################################


def jugar_niveles_demo(niveles: list, cantidad_niveles_demo: int, partidas_por_nivel: int):
    """
    Función para jugar un número limitado de niveles en modo DEMO.
    """

    puntaje_total = 0
    i_nivel = 0
    resultado_final = None

    # calcular límite de niveles a jugar
    if len(niveles) < cantidad_niveles_demo:
        limite = len(niveles)
    else:
        limite = cantidad_niveles_demo

    while i_nivel < limite:
        nivel = niveles[i_nivel]
        print("\n=== NIVEL " + str(nivel["nivel"]) + " ===\n")

        puntos = jugar_nivel_demo(nivel, partidas_por_nivel)

        # detectar salida
        if puntos == "salir":
            resultado_final = "salir"
            break

        # sumar puntaje
        puntaje_total = puntaje_total + puntos

        print("--- FIN DEL NIVEL", nivel["nivel"], "---")
        print("Puntaje acumulado:", puntaje_total, "\n")

        i_nivel = i_nivel + 1

    if resultado_final == None:
        resultado_final = puntaje_total

    return resultado_final


def jugar_nivel_demo(nivel: dict, partidas_por_nivel: int) -> int | str:
    puntaje_total = 0
    cantidad_jugadas = 0
    salida_final = None

    while cantidad_jugadas < partidas_por_nivel:

        datos_partida = buscar_partida_aleatoria_sin_repetir(nivel)

        #Mok de datos para la demo
        print("Palabras válidas para esta partida:", datos_partida["validas"])

        datos_partida["nivel"] = nivel

        resultado = jugar_partida(datos_partida)
        tipo, valor = procesar_resultado_partida(resultado, nivel)

        if tipo == "salir":
            salida_final = "salir"
            break

        if tipo == "accion":
            # cambiar_partida → no sumar, no avanzar
            continue

        # puntaje
        puntaje_total = puntaje_total + valor
        cantidad_jugadas = cantidad_jugadas + 1

    if salida_final == None:
        salida_final = puntaje_total

    return salida_final



def jugar_niveles(niveles: list):
    """
    Función para jugar todos los niveles en modo completo.
    """

    puntaje_total = 0
    i_nivel = 0
    resultado_final = None

    while i_nivel < len(niveles):
        nivel = niveles[i_nivel]
        print("\n=== NIVEL " + str(nivel["nivel"]) + " ===\n")

        puntos = jugar_nivel(nivel, len(nivel["partidas"]))

        # detectar salida
        if puntos == "salir":
            resultado_final = "salir"
            break

        # sumar puntaje
        puntaje_total = puntaje_total + puntos

        print("--- FIN DEL NIVEL", nivel["nivel"], "---")
        print("Puntaje acumulado:", puntaje_total, "\n")

        i_nivel = i_nivel + 1

    if resultado_final is None:
        resultado_final = puntaje_total

    return resultado_final



def jugar_nivel(nivel: dict, partidas_por_nivel: int) -> int | str:
    puntaje_total = 0
    cantidad_jugadas = 0
    salida_final = None

    while cantidad_jugadas < partidas_por_nivel:

        datos_partida = buscar_partida_aleatoria_sin_repetir(nivel)
        datos_partida["nivel"] = nivel

        resultado = jugar_partida(datos_partida)
        tipo, valor = procesar_resultado_partida(resultado, nivel)

        if tipo == "salir":
            salida_final = "salir"
            break

        if tipo == "accion":
            # cambiar_partida
            continue

        puntaje_total = puntaje_total + valor
        cantidad_jugadas = cantidad_jugadas + 1

    if salida_final == None:
        salida_final = puntaje_total

    return salida_final
