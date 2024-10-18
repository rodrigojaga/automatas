from fpdf import FPDF

'''
P : portrait (vertical)
L : landscape (horizontal)

A4 : 210x297mm
'''

#P -> vertical, L -> Horizontal
pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
pdf.add_page()

pdf.rect(x= 10, y= 10, w= 190, h= 277)


# TEXTO  -----
linea = 15
pdf.set_font('Arial','',18)

pdf.text(x= 11, y= linea, txt='Rodrigo Javier Galindo Santos')
linea += 7
pdf.text(x= 11, y= linea, txt='Carlos Alexander Lemus Palencia')
linea += 7
pdf.text(x= 11, y= linea, txt='Irvin Josue Diaz')
linea += 20
pdf.set_font('Arial','UB',18)
pdf.text(x= 78, y= linea, txt='Resolviendo un AFD')

# IMAGEN (jpg/png) -----
pdf.image('logoU.png',
        x= 170, y= 11,
        w = 30, h = 30)


pdf.set_font('Arial','',12)
linea += 20
pdf.text(x= 11, y= linea, txt='La 5-tupla del automata (Q, S, d, q0, F) se resuelve: ')

pdf.output('hoja.pdf')