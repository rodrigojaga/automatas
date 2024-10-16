import matplotlib.pyplot as plt

class controllerFunction:
    def mostrarImagen(self):

        image_path = 'C:/cursoPythonudemy/automatas/output/automata.png'
        img = plt.imread(image_path)
        plt.imshow(img)
        plt.show()