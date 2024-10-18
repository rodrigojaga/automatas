from fpdf import FPDF
import random

class CrearPDF:
    def __init__(self):
        self.pdf = FPDF(orientation='P', unit='mm', format='A4')
        self.linea = 15
        self.pdf.add_page()

        # Dibujar un rectángulo alrededor de la página
        self.pdf.rect(x=10, y=10, w=190, h=277)

        self.pdf.set_font('Arial', '', 18)
        self.pdf.text(x=11, y=self.linea, txt='Rodrigo Javier Galindo Santos')
        self.linea += 7
        self.pdf.text(x=11, y=self.linea, txt='Carlos Alexander Lemus Palencia')
        self.linea += 7
        self.pdf.text(x=11, y=self.linea, txt='Irvin Josue Diaz')
        self.linea += 20
        self.pdf.set_font('Arial', 'UB', 18)
        self.pdf.text(x=78, y=self.linea, txt='Resolviendo un AFD')

        # Imagen (logo)
        self.pdf.image('C:/cursoPythonudemy/automatas/pdf/logoU.png', x=170, y=11, w=30, h=30)

        self.pdf.set_font('Arial', '', 12)
        self.linea += 20
        self.pdf.text(x=11, y=self.linea, txt='La 5-tupla del automata (Q, S, d, q0, F) se resuelve: ')
        self.linea += 5

    def insertarEstados(self, estados: list):
        self.pdf.text(x=16, y=self.linea, txt='Estados (Q): ')
        self.linea += 5
        for estado in estados:
            self.pdf.text(x=16, y=self.linea, txt=f'{estado}')
            self.linea += 4

    def insertarAlfabeto(self, alfabeto: list):
        elementos_unicos = set(alfabeto)

        self.pdf.text(x=16, y=self.linea, txt='Alfabeto (S): ')
        self.linea += 5
        for simbolo in elementos_unicos:
            self.pdf.text(x=16, y=self.linea, txt=f'{simbolo}')
            self.linea += 4

    def insertarEstadoInicial(self, estado_inicial):
        self.pdf.text(x=16, y=self.linea, txt='Estado Inicial (q0): ')
        self.linea += 5
        self.pdf.text(x=16, y=self.linea, txt=f'{estado_inicial}')
        self.linea += 5

    def insertarEstadosAceptacion(self, estados_aceptacion: list):
        self.pdf.text(x=16, y=self.linea, txt='Estados de aceptacion (F): ')
        self.linea += 5
        for eA in estados_aceptacion:
            self.pdf.text(x=16, y=self.linea, txt=f'{eA}')
            self.linea += 4

    def insertarTransiciones(self, transiciones: dict):
        self.pdf.add_page()
        self.pdf.rect(x=10, y=10, w=190, h=277)
        self.linea = 15
        self.pdf.text(x=16, y=self.linea, txt='Transiciones (d): ')
        self.linea += 5
        for clave, valor in transiciones.items():
            texto = f"({clave[0]}, '{clave[1]}'): '{valor}'"
            self.pdf.text(x=16, y=self.linea, txt=texto)
            self.linea += 10

    def insertarImagen(self):
        self.pdf.add_page()
        self.pdf.rect(x=10, y=10, w=190, h=277)
        self.pdf.image('C:/cursoPythonudemy/automatas/output/automata.png', x=11, y=11, w=150, h=150)

    def insertarCadenas(self, cadenas: dict):
        self.pdf.add_page()
        self.pdf.rect(x=10, y=10, w=190, h=277)
        self.linea = 15
        self.pdf.text(x=16, y=self.linea, txt='Cadenas Ingresadas en el automata: ')
        self.linea += 5
        for clave, valor in cadenas.items():
            texto = ''
            resultado = next(iter(valor))
            if resultado:
                texto = f"{clave} fue ACEPTADA por el automata"
            else:
                texto = f"{clave} fue RECHAZADA por el automata"
            self.pdf.text(x=16, y=self.linea, txt=texto)
            self.linea += 10

    def crearPDFArchivo(self):
        direccion = 'C:/Users/rodri/OneDrive/Desktop/automatasPDF/'+'automataResuelto'+str(random.randint(1, 100))+'.pdf'
        self.pdf.output(direccion)
