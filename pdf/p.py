from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from graphviz import Digraph
import controllerFunction as cF
from clases import transicion, estado

dot = Digraph(comment='AFD')
cFI = cF.controllerFunction()
con = ''
estados = []

# Función para la interfaz gráfica
def agregar_estado():
    estado_nombre = estado_entry.get().replace(' ', '')
    if estado_nombre:
        if estado_nombre not in [e.nombreEstado for e in estados]:
            nuevo_estado = estado(estado_nombre, False)
            estados.append(nuevo_estado)
            estado_listbox.insert(END, estado_nombre)
            estado_entry.delete(0, END)
        else:
            messagebox.showwarning("Estado duplicado", "El estado ya existe.")
    else:
        messagebox.showwarning("Campo vacío", "Ingrese un nombre de estado.")

def agregar_transicion():
    origen = origen_entry.get().replace(' ', '')
    simbolo = simbolo_entry.get().replace(' ', '')
    destino = destino_entry.get().replace(' ', '')

    if len(origen) > 0 and len(simbolo) == 1 and len(destino) > 0:
        transicion_temp = transicion(origen, simbolo, destino)
        dot.edge(transicion_temp.estadoOrigen, transicion_temp.estadoDestino, label=transicion_temp.simboloTransicion)
        transicion_str = f'{origen} -> {simbolo} -> {destino}'
        transicion_listbox.insert(END, transicion_str)
        origen_entry.delete(0, END)
        simbolo_entry.delete(0, END)
        destino_entry.delete(0, END)
    else:
        messagebox.showerror("Error", "Verifique que los datos estén correctos y completos.")

# Mostrar imagen en la interfaz gráfica
def mostrar_imagen():
    ruta_imagen = filedialog.askopenfilename(title="Selecciona la imagen", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if ruta_imagen:
        img = Image.open(ruta_imagen)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        imagen_label.config(image=img_tk)
        imagen_label.image = img_tk

# Función que muestra un mensaje en la interfaz
def mostrar_mensaje():
    messagebox.showinfo("Información", "Ejemplo de cómo puede ingresar las relaciones: q0-0-q1, q1-1-q0")

# Crear ventana principal
ventana = Tk()
ventana.title("Automata con Tkinter")
ventana.geometry("600x700")

# Área de ingreso de estados
estado_frame = LabelFrame(ventana, text="Agregar Estados", padx=10, pady=10)
estado_frame.pack(padx=10, pady=10)

estado_entry = Entry(estado_frame)
estado_entry.grid(row=0, column=0, padx=10, pady=5)

agregar_estado_btn = Button(estado_frame, text="Agregar Estado", command=agregar_estado)
agregar_estado_btn.grid(row=0, column=1, padx=10)

estado_listbox = Listbox(estado_frame)
estado_listbox.grid(row=1, column=0, columnspan=2, pady=10)

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

agregar_transicion_btn = Button(transicion_frame, text="Agregar Transición", command=agregar_transicion)
agregar_transicion_btn.grid(row=3, column=0, columnspan=2, pady=10)

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

# Iniciar la aplicación
ventana.mainloop()
