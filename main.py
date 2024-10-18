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
transiciones = []


def crearAutomata():
    # estados = []
    # con = ''

    # print('Primero declararemos los estados')

    # while con.lower() != 'no':
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
                    estadoTemp = estado(lsX[i], False, False)
                    estados.append(estadoTemp)
                    estado_listbox.insert(END, lsX[i])
                    estadoDeAceptacionUnico(estadoTemp)
                    estadoInicial(estadoTemp)
            estado_entry.delete(0, END)  # Limpiar la entrada

        else:
            # Verificar si el estado corto ya está en la lista
            if x in [estado.nombreEstado for estado in estados]:
                messagebox.showwarning('Estado existente', f'El estado {x} ya ha sido ingresado')
            else:
                estadoNuevo = estado(x, False, False)
                estados.append(estadoNuevo)
                estado_listbox.insert(END, x)
                estado_entry.delete(0, END)  # Limpiar la entrada
                estadoDeAceptacionUnico(estadoNuevo)
                estadoInicial(estadoNuevo)


    else:
        messagebox.showwarning("Campo vacío", "Ingrese un nombre de estado.")

        # con = input('Desea agregar otro estado? (Si/No)')

    # Cargar los estados ingresados en el autómata
    cargarEstadosAutomata(estados)

    # llamarImagen()

    # Ingresamos las transiciones entre estados
    # indicarRelaciones()


def estadoDeAceptacionUnico(estadoAc: estado):
    isAceptacion = bool(var.get())
    if isAceptacion:
        etiqueta.config(text=f"El estado {estadoAc.nombreEstado} es un estado de aceptacion")
        for i in range(len(estados)):
            if estadoAc.nombreEstado == estados[i].nombreEstado:
                estados[i].isAceptacion = True
    else:
        etiqueta.config(text="No se ha elegido ningun estado de aceptacion")


def estadoInicial(estadoAc: estado):
    isAceptacion = bool(varInicio.get())
    if isAceptacion:
        etiquetaInicial.config(text=f"El estado {estadoAc.nombreEstado} es el estado inicial")
        for i in range(len(estados)):
            if estadoAc.nombreEstado == estados[i].nombreEstado:
                estados[i].isInicio = True
    else:
        etiquetaInicial.config(text="No se ha elegido ningun estado Inicial")


# Función que agrega los estados al autómata
def cargarEstadosAutomata(estados: list):
    for estado in estados:
        if estado.isAceptacion and not estado.isInicio:
            dot.node(estado.nombreEstado, estado.nombreEstado, style='filled', fillcolor='green', color='red')
        elif estado.isInicio and not estado.isAceptacion:
            dot.node(estado.nombreEstado, estado.nombreEstado, style='filled', fillcolor='lightblue', color='purple')
        elif estado.isInicio and estado.isAceptacion:
            dot.node(estado.nombreEstado, estado.nombreEstado, style='filled', fillcolor='lightblue', color='red')
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
            # ingresarRelaciones(transiciones)
        else:  # Caso 2: Ingreso secuencial
            estadoOrigen = x
            simbolo = input('Ingrese el símbolo de transición (1 carácter): ')

            while len(simbolo) != 1:
                simbolo = input('Debe ingresar un símbolo de 1 carácter: ')

            estadoDestino = input('Ingrese el estado destino: ').replace(' ', '')
            # print(f"Transición agregada: {estado_origen} -> {simbolo} -> {estado_destino}")

            ingresarRelacionesS(estadoOrigen, simbolo, estadoDestino)

        con = input('¿Desea agregar otra transición? (Si/No)')

    llamarImagen()


def ingresarRelacionesS():
    origen = origen_entry.get().replace(' ', '')
    simbolo = simbolo_entry.get().replace(' ', '')
    destino = destino_entry.get().replace(' ', '')

    if len(origen) > 0 and len(simbolo) == 1 and len(destino) > 0:
        existeOrigen = False
        existeDestino = False
        for i in estados:
            if origen == i.nombreEstado and destino != origen:
                existeOrigen = True
            elif destino == i.nombreEstado and destino != origen:
                existeDestino = True
            elif origen == destino:
                existeOrigen = True
                existeDestino = True

        if existeOrigen and existeDestino:
            transicionTmp = transicion(origen, simbolo, destino)
            transiciones.append(transicionTmp)
            dot.edge(transicionTmp.estadoOrigen, transicionTmp.estadoDestino, label=transicionTmp.simboloTransicion)
            transicion_str = f'{origen} -> {simbolo} -> {destino}'
            transicion_listbox.insert(END, transicion_str)
            origen_entry.delete(0, END)
            simbolo_entry.delete(0, END)
            destino_entry.delete(0, END)
        elif not existeOrigen:
            messagebox.showerror("Error", "El estado origen no existe")
        elif not existeDestino:
            messagebox.showerror("Error", "El estado destino no existe")
        else:
            messagebox.showerror("Error", "Estados no existen")
    else:
        messagebox.showerror("Error", "Verifique que los datos estén correctos y completos.")


"""
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

"""


def llamarImagen():
    # Generar imagen después de cargar los estados
    hacerImagen()
    cFI.mostrarImagen()




# Mostrar imagen en la interfaz gráfica
def mostrar_imagen():
    hacerImagen()
    # ruta_imagen = filedialog.askopenfilename(title="Selecciona la imagen", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    # if ruta_imagen:
    img = Image.open('C:/cursoPythonudemy/automatas/output/automata.png')
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    imagen_label.config(image=img_tk)
    imagen_label.image = img_tk


# Crear ventana principal
ventana = Tk()
ventana.title("Automata con Tkinter")
ventana.geometry("800x650")

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
varInicio = IntVar()

# Crear el Checkbutton para estados de aceptacion
checkbutton = Checkbutton(estado_frame, text="Estado de aceptacion", variable=var)
checkbutton.grid(row=0, column=2, padx=10)
# checkbutton.pack()

# Crear el Checkbutton para estados iniciales
checkbutton = Checkbutton(estado_frame, text="Estado inicial", variable=varInicio)
checkbutton.grid(row=0, column=3, padx=10)

# Etiqueta para mostrar el estado
etiqueta = Label(estado_frame, text="No se ha elegido ningun estado de aceptacion")
etiqueta.grid(row=2, padx=10)
# etiqueta.pack()

# Etiqueta para mostrar el estado inicial
etiquetaInicial = Label(estado_frame, text="No se ha elegido ningun estado inicial")
etiquetaInicial.grid(row=3, padx=10)

# Área de ingreso de transiciones
transicion_frame = LabelFrame(ventana, text="Agregar Transiciones", padx=10, pady=10)
transicion_frame.pack(padx=10, pady=10)

origen_label = Label(transicion_frame, text="Estado Origen:")
origen_label.grid(row=0, column=0, sticky="nw")
origen_entry = Entry(transicion_frame)
origen_entry.grid(row=0, column=1, sticky="nw")

simbolo_label = Label(transicion_frame, text="Símbolo:")
simbolo_label.grid(row=1, column=0, sticky="nw")
simbolo_entry = Entry(transicion_frame)
simbolo_entry.grid(row=1, column=1, sticky="nw")

destino_label = Label(transicion_frame, text="Estado Destino:")
destino_label.grid(row=2, column=0, sticky="ew")
destino_entry = Entry(transicion_frame)
destino_entry.grid(row=2, column=1, sticky="ew")

agregar_transicion_btn = Button(transicion_frame, text="Agregar Transición", command=ingresarRelacionesS)
agregar_transicion_btn.grid(row=3, column=0, sticky="nw")

transicion_listbox = Listbox(transicion_frame)
transicion_listbox.grid(row=4, column=0, sticky="nw")

# Área para cargar y mostrar la imagen
# imagen_frame = LabelFrame(ventana, text="Visualizar Imagen", padx=10, pady=10)
# imagen_frame.grid(row=2,column=2)
# imagen_frame.pack(padx=10, pady=10)

cargar_imagen_btn = Button(transicion_frame, text="Cargar Imagen", command=mostrar_imagen)
cargar_imagen_btn.grid(row=0, column=3)  # pack(pady=5)

imagen_labelIM = Label(transicion_frame, text='')
imagen_labelIM.grid(row=5, column=2, padx=50, sticky="nwe")  # pack(pady=10)

imagen_label = Label(transicion_frame, text='Texto aqui')
imagen_label.grid(row=1, column=3)  # pack(pady=10)

boton = Button(ventana, text="Mostrar imagen", command=llamarImagen)
boton.pack(pady=10)
# Inicia la app
ventana.mainloop()