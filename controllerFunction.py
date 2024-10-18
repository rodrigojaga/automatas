import matplotlib.pyplot as plt
import os

class controllerFunction:
    def mostrarImagen(self):

        image_path = 'C:/cursoPythonudemy/automatas/output/automata.png'
        img = plt.imread(image_path)
        plt.imshow(img)
        plt.show()

    def borrarAutomata(self):
        rutaImagen = 'C:/cursoPythonudemy/automatas/output/automata.png'
        if os.path.exists(rutaImagen):
            os.remove(rutaImagen)
            return 'Automata eliminado'
        else:
            return 'Automata no existe'