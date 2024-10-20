from graphviz import Digraph
import controllerFunction as cF
from tkinter import *
import tkinter as tk
from clases import transicion, estado, automata
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from pdf.p import CrearPDF
import os

dot = Digraph(comment='AFD')
cFI = cF.controllerFunction()
con = ''
estados = []
transiciones = []
cadenasAceptadasAutomata = {}


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
                return 

            for i in range(len(lsX)):                
                if lsX[i] in [estado.nombreEstado for estado in estados]:
                    messagebox.showwarning('Estado existente', f'El estado {lsX[i]} ya ha sido ingresado')
                else:                    
                    estadoTemp = estado(lsX[i], False, False)
                    estados.append(estadoTemp)
                    estado_listbox.insert(END, lsX[i])
                    estadoDeAceptacionUnico(estadoTemp)
                    estadoInicial(estadoTemp)
            estado_entry.delete(0, END)

        else:
            
            if x in [estado.nombreEstado for estado in estados]:
                messagebox.showwarning('Estado existente', f'El estado {x} ya ha sido ingresado')
            else:
                estadoNuevo = estado(x, False, False)
                estados.append(estadoNuevo)
                estado_listbox.insert(END, x)
                estado_entry.delete(0, END)  
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


# Funcion que agrega los estados al automata
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


# Funcion para generar la imagen
def hacerImagen():
    dot.render('output/automata', format='png')  
    print(dot.source) 





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


def llamarImagen():
    
    hacerImagen()
    cFI.mostrarImagen()




# Mostrar imagen en la interfaz grafica
def mostrar_imagen():
    hacerImagen()
    img = Image.open('C:/cursoPythonudemy/automatas/output/automata.png')
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    imagen_label.config(image=img_tk)
    imagen_label.image = img_tk

def limpiarTodo():
    global estados, transiciones
    estados.clear()
    transiciones.clear()
    messagebox.showinfo('Automata', cFI.borrarAutomata())
    imagen_label.config(image='',text='Esperando...')
    print(estados)
    print(transiciones)
    estado_listbox.delete(first=0,last=END)
    transicion_listbox.delete(first=0,last=END)

#Toma la cadena y la prueba en el automata
def probarCadena():
    global cadenasAceptadasAutomata
    cadena = entradaCadena.get().replace(' ', '')
    if not cadena:
        messagebox.showerror('Error', 'Debe ingresar una cadena')
    else:
        automata = crearAutomataObjeto()
        if not automata.procesar_cadena(cadena):
            messagebox.showinfo('Cadena', f'El automata ha RECHAZADO la cadena {cadena}')
            cadenasAceptadasAutomata[cadena] = {False}
        else:
            messagebox.showinfo('Cadena', f'El automata ha ACEPTADO la cadena {cadena}')
            cadenasAceptadasAutomata[cadena] = {True}


#Funcion que crea el objeto automata
def crearAutomataObjeto():
    automataObj = automata(crearListaEstados(), crearAlfabeto(), crearTransiciones(), crearEstadoInicial(), crearEstadoAceptacion())
    return automataObj


#Funciones que sirven para definir un objeto 'automata'
def crearListaEstados():
    global estados
    nEstados = []
    if not estados:
        messagebox.showerror('Lista Vacia', 'No se tiene ningun estado aun')
        return nEstados  
    else:
        for estado in estados:
            nEstados.append(estado.nombreEstado)
        return nEstados

def crearAlfabeto():
    global transiciones
    nAlfabeto = []
    if not transiciones:
        messagebox.showerror('Lista Vacia', 'No se tiene ninguna transicion aun')
        return nAlfabeto 
    else:
        for simbolo in transiciones:
            nAlfabeto.append(simbolo.simboloTransicion)
        return nAlfabeto

def crearEstadoAceptacion():
    global estados
    nEstadosAceptacion = []
    if not estados:
        messagebox.showerror('Lista Vacia', 'No se tiene ningun estado aun')
        return nEstadosAceptacion  
    else:
        for estado in estados:
            if estado.isAceptacion:
                nEstadosAceptacion.append(estado.nombreEstado)
        return nEstadosAceptacion

def crearEstadoInicial():
    global estados
    q0 = ''
    if not estados:
        messagebox.showerror('Lista Vacia', 'No se tiene ningun estado aun')
        return q0  
    else:
        for estado in estados:
            if estado.isInicio:
                q0 = estado.nombreEstado
                break
        return q0

def crearTransiciones():
    global transiciones
    transicionesDict = {}
    if not transiciones:
        messagebox.showerror('Lista Vacia', 'No se tiene ninguna transicion aun')
        return transicionesDict  
    else:
        for transicion in transiciones:
            clave = (transicion.estadoOrigen, transicion.simboloTransicion)
            transicionesDict[clave] = transicion.estadoDestino
        return transicionesDict


def exportarPDF():
    global cadenasAceptadasAutomata
    pdf = CrearPDF()
    pdf.insertarEstados(crearListaEstados())
    pdf.insertarAlfabeto(crearAlfabeto())
    pdf.insertarEstadoInicial(crearEstadoInicial())
    pdf.insertarEstadosAceptacion(crearEstadoAceptacion())
    pdf.insertarTransiciones(crearTransiciones())
    pdf.insertarImagen()
    pdf.insertarCadenas(cadenasAceptadasAutomata)
    pdf.crearPDFArchivo()

    print(cadenasAceptadasAutomata)
    messagebox.showinfo('PDF CREADO', 'El PDF ha sido creado')
# Crear ventana principal
ventana = Tk()
ventana.title("Automata con Tkinter")
ventana.geometry("1000x700")

framePrincipal = LabelFrame(ventana, text='Crear Automata')
framePrincipal.pack()
# area de ingreso de estados
estado_frame = LabelFrame(framePrincipal, text="Agregar Estados", padx=10, pady=10)
estado_frame.grid(row=0,column=0,padx=10, pady=10)

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

# area de ingreso de transiciones
transicion_frame = LabelFrame(framePrincipal, text="Agregar Transiciones", padx=10, pady=10)
transicion_frame.grid(row=0,column=1,padx=10, pady=10)

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

# area para cargar y mostrar la imagen

frameSecundario = LabelFrame(ventana)
frameSecundario.pack(pady=10)

cargar_imagen_btn = Button(frameSecundario, text="Cargar Imagen", command=mostrar_imagen)
cargar_imagen_btn.grid(row=0, column=3,padx=10)  # pack(pady=5)

pdfBtn = Button(frameSecundario, text="Exporta como PDF", command=exportarPDF)
pdfBtn.grid(row=0, column=4,padx=10)  # pack(pady=5)

imagen_labelIM = Label(frameSecundario, text='')
imagen_labelIM.grid(row=1)  # pack(pady=10)

imagen_label = Label(frameSecundario, text='Esperando...')
imagen_label.grid(row=1)  # pack(pady=10)

extraFrame= LabelFrame(frameSecundario, text="Opciones adicionales", padx=10, pady=10)
extraFrame.grid(row=0, column=0)
boton = Button(extraFrame, text="Mostrar imagen", command=llamarImagen)
boton.grid(row=0,pady=10, padx=10)

botonLimpiar = Button(extraFrame, text="LIMPIAR TODO", command=limpiarTodo)
botonLimpiar.grid(row=0, column=1,pady=10, padx=10)


entradaLabel = Label(extraFrame, text='Ingresar Cadena de prueba')
entradaLabel.grid(row=1,column=0)
entradaCadena = Entry(extraFrame)
entradaCadena.grid(row=1,column=1)
botonProbarCadena = Button(extraFrame, text='Probar cadena en el automata', command=probarCadena)
botonProbarCadena.grid(row=2)


# Inicia la app
ventana.mainloop()
