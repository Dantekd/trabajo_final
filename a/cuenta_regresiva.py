# MODULO PARA HACER LA CUENTA REGRESIVA - TIEMPO???

import time


def contar_regresivo(segundos:int) -> bool:
    inicio = time.time()
    fin = inicio + segundos
    bandera = False
    ultimo_segundo = segundos  # controla para no repetir prints
    while time.time() < fin:
        tiempo_restante = int(fin - time.time())


        if tiempo_restante != ultimo_segundo: # Imprimir solo cuando cambia el segundo
            print("Tiempo:", tiempo_restante)
            ultimo_segundo = tiempo_restante

        chale=input("inGRESA algo")
        print(chale)

    bandera = True
    return bandera

# bandera = contar_regresivo(10)
# print("Terminado:", bandera)





def funcion_cuenta_regresiva(segundos:int):
    inicio = time.time()
    fin = inicio + segundos
    ultimo_segundo = segundos

    while time.time() < fin:
        tiempo_restante = int(fin - time.time())

        # Avisar al programa principal que cambió un segundo
        if tiempo_restante != ultimo_segundo:
            ultimo_segundo = tiempo_restante
            yield ultimo_segundo  # devuelve el tiempo sin cortar la función

    yield 0



#print segun tieempo.
# 
