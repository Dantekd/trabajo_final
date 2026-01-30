#CONTADOR DE COSAS PARA VER: 2

from validaciones import validar_palabra

from numericas import sumar_puntaje, acumular_ingresos_incorrectos

#Esto crea lo datos que puede llegar a haber dentro del juego 

def crear_estado_pygame(base_lista, palabras_validas):
    estado = {
        "base_lista": base_lista,
        "palabras_validas": palabras_validas,
        "palabras_ingresadas": [],
        "palabras_encontradas": [],
        "puntaje": 0,
        "errores": 0,
        "intentos_maximos": 5,
        "ultimo_resultado": "", #fijarte si es correcto
        "comodin_revelar": True,
        "comodin_ubicar": True
    }
    return estado

#Esto precesa la cantidad de palabra aun no descubiertas.

def procesar_palabra_pygame(estado, palabra):
    resultado = ""

    palabra_minus = palabra.lower()
    repetida = False

    i = 0
    while i < len(estado["palabras_ingresadas"]):#hace que el contador disminuya de si llegaste a descubrir una palabra correcta
        if estado["palabras_ingresadas"][i] == palabra_minus:
            repetida = True
        i = i + 1

    if repetida:
        resultado = "repetida"
    #palabra_minus saber explicar
    else:
        es_valida = validar_palabra(#Esto valida si la palabra que se ingresa esra dentro 
            palabra_minus,
            estado["base_lista"],
            estado["palabras_validas"]
        )

        if es_valida:
            estado["puntaje"] = sumar_puntaje(estado["puntaje"], palabra_minus)
            estado["palabras_encontradas"].append(palabra_minus)
            resultado = "valida"
        else:
            estado["errores"] = acumular_ingresos_incorrectos(
                estado["errores"],es_valida
            )
            resultado = "invalida"

        estado["palabras_ingresadas"].append(palabra_minus)

    estado["ultimo_resultado"] = resultado
    return resultado


def verificar_fin_pygame(estado):
    terminado = False

    if estado["errores"] >= estado["intentos_maximos"]:
        terminado = True

    if len(estado["palabras_encontradas"]) >= len(estado["palabras_validas"]):
        terminado = True

    return terminado
