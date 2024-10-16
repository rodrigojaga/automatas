from graphviz import Digraph
import controllerFunction as cF
from tkinter import *
from clases import transicion, estado

dot = Digraph(comment='AFD')
cFI = cF.controllerFunction()
con = ''


def crearAutomata():
    estados = []
    con = ''

    print('Primero declararemos los estados')
    while con.lower() != 'no':
        x = (input('Nombre/s estado/s: ')).replace(' ', '')
        if len(x) > 3:
            lsX = []
            if '-' in x:
                lsX = x.split('-')
            elif ',' in x:
                lsX = x.split(',')
            elif '/' in x:
                lsX = x.split('/')
            else:
                print('Ingrese un formato de separacion acceptable (/ , -)')

            for i in range(0,len(lsX)):
                estadoTemp = estado(lsX[i], False)
                estados.append(estadoTemp)
        else:
            estados.append(estado(x, False))

        con = input('Desea agregar otro estado? (Si/No)')
    print('Cual de estos es un estado de aceptacion?: ')
    v = ''
    for es in range(len(estados)):
        if es == len(estados) -1:
            v+= estados[es].nombreEstado
        else:
            v += estados[es].nombreEstado+', '
    print(v)
    qS = input('-> ')
    for x in estados:
        if qS == x.nombreEstado:
            x.isAceptacion = True
            break


    # Cargar los estados ingresados en el autómata
    cargarEstadosAutomata(estados)

    llamarImagen()

    # Ingresamos las transiciones entre estados
    indicarRelaciones()

# Función que agrega los estados al autómata
def cargarEstadosAutomata(estados: list):
    for estado in estados:
        if estado.isAceptacion:
            dot.node(estado.nombreEstado, estado.nombreEstado, style='filled', fillcolor='green', color='red')
        else:
            dot.node(estado.nombreEstado, estado.nombreEstado)


# Función para generar la imagen
def hacerImagen():
    dot.render('output/automata', format='png')  # Genera la imagen PNG
    print(dot.source)  # Muestra el código fuente del gráfico


def indicarRelaciones():
    print('Ahora definamos las relaciones entre estados')
    # cFI.mostrarImagen() # Asegúrate de que este método esté definido si lo necesitas
    con = ''
    print("""
        Ejemplo de cómo puede ingresar las relaciones. Siendo:
            - q0 el estado de origen
            - q1 el estado destino
            - x el símbolo de transición (puede ser cualquier símbolo primitivo, a excepción de λ y ε)
            q0 -> q1
            Ingrese los valores separados por guiones o comas, al acabar con la transición puede utilizar un guion para definir otra relación:
            Ejemplo de Caso 1: q0-0-q1, q1-1-q0, q3-0-q2
            O puede ingresarlo de manera separada, siguiendo el orden de:
            1. Ingresar el estado de origen
            2. Ingresar el símbolo de transición
            3. Ingresar el estado destino
    """)

    while con.lower() != 'no':
        x = input('Ingrese la transición o las transiciones: ').replace(' ', '')  # Eliminar espacios en blanco
        if '-' in x or ',' in x:  # Caso 1: múltiples transiciones separadas por guiones/comas
            # Separar por comas o guiones
            transiciones = x.split(',')
            ingresarRelaciones(transiciones)
        else:  # Caso 2: Ingreso secuencial
            estadoOrigen = x
            simbolo = input('Ingrese el símbolo de transición (1 carácter): ')

            while len(simbolo) != 1:
                simbolo = input('Debe ingresar un símbolo de 1 carácter: ')

            estadoDestino = input('Ingrese el estado destino: ').replace(' ', '')
            #print(f"Transición agregada: {estado_origen} -> {simbolo} -> {estado_destino}")

            ingresarRelacionesS(estadoOrigen, simbolo, estadoDestino)

        con = input('¿Desea agregar otra transición? (Si/No)')

    llamarImagen()

def ingresarRelacionesS(estadoOrigen, simboloTransicion, estadoDestino):
    # Cambiar el nombre de la variable 'transicion' a 'simboloTransicion'
    transicionTemp = transicion(estadoOrigen, simboloTransicion, estadoDestino)
    dot.edge(transicionTemp.estadoOrigen, transicionTemp.estadoDestino, label=transicionTemp.simboloTransicion)


def ingresarRelaciones(transiciones: list):
    for trans in transiciones:
        partes = trans.split('-')
        if len(partes) == 3:
            estadoOrigen = partes[0]
            simboloTransicion = partes[1]  # Renombrar la variable 'transicion' a 'simboloTransicion'
            estadoDestino = partes[2]
            transicionTemp = transicion(estadoOrigen, simboloTransicion, estadoDestino)
            #print(f"Transición agregada: {estado_origen} -> {simbolo} -> {estado_destino}")
            dot.edge(transicionTemp.estadoOrigen, transicionTemp.estadoDestino, label=transicionTemp.simboloTransicion)
        else:
            print(f"Error en la transición: {trans}")



def llamarImagen():
    # Generar imagen después de cargar los estados
    hacerImagen()
    cFI.mostrarImagen()



# Bucle principal
while con.lower() != 'no':
    print('Seleccione una opción: ')
    print('1. Ingresar un Autómata')
    print('2. Salir')
    con = input('-> ')

    if con == '1':
        crearAutomata()
    elif con == '2':
        exit()
    else:
        print("Opción no válida. Intente nuevamente.")

"""
dot.node('q1', 'q1')
        dot.node('q2', 'q2')
        dot.node(x, x)
    #dot.edge('q1', 'q2', label='0')
    #dot.edge('q2', 'q1', label='1')
    #dot.edge('q1', 'q1', label='x')
"""
