from labels import Specification, Sheet
from reportlab.graphics import shapes


def desenha(label, width, height, obj):
    """organize the label to print"""
    # Just convert the object to a string and print this at the bottom left of the label.
    if type(obj) == int:
        label.add(shapes.String(0, 0, str()))
    else:
        label.add(shapes.String(width/2-10, height - 15, 'IFPR', fontName="Helvetica", fontSize=10))
        label.add(shapes.String(4, height - 25, 'Nome: ' + obj.pessoa, fontName="Helvetica", fontSize=5))
        label.add(shapes.String(4, height - 35, 'Matricula: ' + str(obj.matricula), fontName="Helvetica", fontSize=6))
        label.add(shapes.String(4, height - 45, obj.curso, fontName="Helvetica", fontSize=5))
        label.add(shapes.String(4, height - 55, 'Cartão: ' + str(obj.cartao), fontName="Helvetica", fontSize=6))
        label.add(shapes.String(width / 2 - 20, 5, 'Curitiba', fontName="Helvetica", fontSize=10))


def criar_etiquetas(df):
    print('Posição da primeira etiqueta em branco:')
    posicao = int(input()) - 1
    # Create a letter portrait (216mm x 279mm) sheets with 3 columns and 10 rows of
    # labels. Each label is 66.7mm x 25.4mm with a 2mm rounded corner.
    specs = Specification(216, 279, 3, 10, 66.7, 25.4, corner_radius=2,
                          left_margin=5, right_margin=4.9, top_margin=13, bottom_margin=12, column_gap=3)
    # create pages with the drawable function
    sheet = Sheet(specs, desenha, border=True)
    # add labels with iterator
    sheet.add_labels(range(posicao))
    sheet.add_labels(df.itertuples())
    # save pdf
    sheet.save('etiqueta.pdf')
