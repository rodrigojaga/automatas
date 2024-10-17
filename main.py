from graphviz import Digraph
import controllerFunction as cF
from tkinter import *
import tkinter as tk
from clases import transicion, estado
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

dot = Digraph(comment='AFD')
cFI = cF.controllerFunction()
con = ''
estados = []

def crearAutomata():
    #estados = []
    #con = ''

    #print('Primero declararemos los estados')

    #while con.lower() != 'no':
    x = estado_entry.get().replace(' ', '')
    if x:
        if len(x) > 3:
            lsX = []
            if '-' in x:
                lsX = x.split('-')
            elif ',' in x:
                lsX = x.split(',')
            elif '/' in x:
                lsX = x.split('/')
            else:
                messagebox.showwarning('Formato incorrecto', 'Ingrese un formato de separación aceptable (/ , -)')
                return  # Sale si el formato no es válido

            for i in range(len(lsX)):
                # Verificar si el estado ya está en la lista 'estados'
                if lsX[i] in [estado.nombreEstado for estado in estados]:
                    messagebox.showwarning('Estado existente', f'El estado {lsX[i]} ya ha sido ingresado')
                else:
                    # Agregar el estado a la lista y al listbox
                    estadoTemp = estado(lsX[i], False)
                    estados.append(estadoTemp)
                    estado_listbox.insert(END, lsX[i])
                    estadoDeAceptacionUnico(estadoTemp)
            estado_entry.delete(0, END)  # Limpiar la entrada

        else:
            # Verificar si el estado corto ya está en la lista
            if x in [estado.nombreEstado for estado in estados]:
                messagebox.showwarning('Estado existente', f'El estado {x} ya ha sido ingresado')
            else:
                estadoNuevo = estado(x, False)
                estados.append(estadoNuevo)
                estado_listbox.insert(END, x)
                estado_entry.delete(0, END)  # Limpiar la entrada
                estadoDeAceptacionUnico(estadoNuevo)


    else:
        messagebox.showwarning("Campo vacío", "Ingrese un nombre de estado.")

        #con = input('Desea agregar otro estado? (Si/No)')


    # Cargar los estados ingresados en el autómata
    cargarEstadosAutomata(estados)

    #llamarImagen()

    # Ingresamos las transiciones entre estados
    #indicarRelaciones()


def estadoDeAceptacionUnico(estadoAc: estado):
    isAceptacion = bool(var.get())
    if isAceptacion:
        etiqueta.config(text=f"El estado {estadoAc.nombreEstado} es un estado de aceptacion")
        for i in range(len(estados)):
            if estadoAc.nombreEstado == estados[i].nombreEstado:
                estados[i].isAceptacion = True
    else:
        etiqueta.config(text="No se ha elegido ningun estado de aceptacion")
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


"""
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

"""
dot.node('q1', 'q1')
        dot.node('q2', 'q2')
        dot.node(x, x)
    #dot.edge('q1', 'q2', label='0')
    #dot.edge('q2', 'q1', label='1')
    #dot.edge('q1', 'q1', label='x')
"""
# Mostrar imagen en la interfaz gráfica
def mostrar_imagen():
    ruta_imagen = filedialog.askopenfilename(title="Selecciona la imagen", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if ruta_imagen:
        img = Image.open('C:/cursoPythonudemy/automatas/output/automata.png')
        img = img.resize((200, 200), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        imagen_label.config(image=img_tk)
        imagen_label.image = img_tk

# Función que muestra un mensaje en la interfaz
def mostrar_mensaje():
    messagebox.showinfo("Información", "Ejemplo de cómo puede ingresar las relaciones: q0-0-q1, q1-1-q0")

"""
# Función para mostrar el estado del Checkbutton
def mostrar_estado():
    estado = var.get()
    if estado == 1:
        etiqueta.config(text="Checkbutton está activado.")
    else:
        etiqueta.config(text="Checkbutton está desactivado.")
"""

# Crear ventana principal
ventana = Tk()
ventana.title("Automata con Tkinter")
ventana.geometry("600x700")

# Área de ingreso de estados
estado_frame = LabelFrame(ventana, text="Agregar Estados", padx=10, pady=10)
estado_frame.pack(padx=10, pady=10)

estado_entry = Entry(estado_frame)
estado_entry.grid(row=0, column=0, padx=10, pady=5)

agregar_estado_btn = Button(estado_frame, text="Agregar Estado", command=crearAutomata)
agregar_estado_btn.grid(row=0, column=1, padx=10)

estado_listbox = Listbox(estado_frame)
estado_listbox.grid(row=1, column=0, columnspan=2, pady=10)

# Variable que guarda el estado del Checkbutton
var = IntVar()

# Crear el Checkbutton
checkbutton = Checkbutton(estado_frame, text="Estado de aceptacion", variable=var)
checkbutton.grid(row=0, column=2, padx=10)
#checkbutton.pack()

# Etiqueta para mostrar el estado
etiqueta = Label(estado_frame, text="No se ha elegido ningun estado de aceptacion")
etiqueta.grid(row=2, padx=10)
#etiqueta.pack()



# Área de ingreso de transiciones
transicion_frame = LabelFrame(ventana, text="Agregar Transiciones", padx=10, pady=10)
transicion_frame.pack(padx=10, pady=10)

origen_label = Label(transicion_frame, text="Estado Origen:")
origen_label.grid(row=0, column=0)
origen_entry = Entry(transicion_frame)
origen_entry.grid(row=0, column=1)

simbolo_label = Label(transicion_frame, text="Símbolo:")
simbolo_label.grid(row=1, column=0)
simbolo_entry = Entry(transicion_frame)
simbolo_entry.grid(row=1, column=1)

destino_label = Label(transicion_frame, text="Estado Destino:")
destino_label.grid(row=2, column=0)
destino_entry = Entry(transicion_frame)
destino_entry.grid(row=2, column=1)

#agregar_transicion_btn = Button(transicion_frame, text="Agregar Transición", command=agregar_transicion)
#agregar_transicion_btn.grid(row=3, column=0, columnspan=2, pady=10)

transicion_listbox = Listbox(transicion_frame)
transicion_listbox.grid(row=4, column=0, columnspan=2, pady=10)

# Botón para mostrar mensajes especiales
mensaje_frame = LabelFrame(ventana, text="Mensajes", padx=10, pady=10)
mensaje_frame.pack(padx=10, pady=10)

mensaje_btn = Button(mensaje_frame, text="Mostrar Mensaje", command=mostrar_mensaje)
mensaje_btn.pack(pady=5)

# Área para cargar y mostrar la imagen
imagen_frame = LabelFrame(ventana, text="Visualizar Imagen", padx=10, pady=10)
imagen_frame.pack(padx=10, pady=10)

cargar_imagen_btn = Button(imagen_frame, text="Cargar Imagen", command=mostrar_imagen)
cargar_imagen_btn.pack(pady=5)

imagen_label = Label(imagen_frame)
imagen_label.pack(pady=10)

#Inicia la app
ventana.mainloop()

