
from mecanicas import *
from numericas import *
from validaciones import *
from flujo_juego import jugar_niveles_demo
from csv_datos import cargar_niveles   
from comodines import *

# JUEGO MAIN -- DEMO.
def main():
    # print solo para la demo.
    print("=== DEMO CONFIGURABLE ===")

    # cargo los niveles del diccionario.
    niveles = cargar_niveles()

    # la cantidad de niveles y partidas a jugar.
    cant_niveles_demo = int(input("Cantidad de niveles a jugar (demo): "))
    partidas_por_nivel = int(input("Cantidad de partidas por nivel (demo): "))

    # el puntaje total a partir de los niveles y partidas.
    puntaje_total = jugar_niveles_demo(niveles, cant_niveles_demo, partidas_por_nivel)

    # prints para la finalización del juego y el respectivo puntaje.
    print("JUEGO FINALIZADO")
    print("Puntaje total:", puntaje_total)

# llamada a main.
if __name__ == "__main__":
    main()

