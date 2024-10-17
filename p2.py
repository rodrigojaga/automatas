from tkinter import Tk, Checkbutton, IntVar, Label

# Crear la ventana principal
root = Tk()
root.title("Ejemplo de Checkbutton")

# Variable que guarda el estado del Checkbutton
var = IntVar()

# Función para mostrar el estado del Checkbutton
def mostrar_estado():
    estado = var.get()
    if estado == 1:
        etiqueta.config(text="Checkbutton está activado.")
    else:
        etiqueta.config(text="Checkbutton está desactivado.")

# Crear el Checkbutton
checkbutton = Checkbutton(root, text="Activar", variable=var, command=mostrar_estado)
checkbutton.pack()

# Etiqueta para mostrar el estado
etiqueta = Label(root, text="Checkbutton está desactivado.")
etiqueta.pack()

# Ejecutar la ventana
root.mainloop()
