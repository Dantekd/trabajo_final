
from mecanicas import *
from numericas import *
from validaciones import *
from flujo_juego import jugar_niveles
from csv_datos import cargar_niveles   

# JUGAR EL JUEGO COMPLETO.
def main():
    # cargo los niveles con sus partidas desde el csv.
    niveles = cargar_niveles()
    # a medida que juego, calculo el puntaje.
    resultado = jugar_niveles(niveles)
    
    # prints para finalizar y mostrar el puntaje total.
    print("JUEGO FINALIZADO")
    
    if resultado == "salir":
        print("El jugador salió manualmente.")
    else:
        print("Puntaje total:", resultado)

# llamada a main.
if __name__ == "__main__":
    main()