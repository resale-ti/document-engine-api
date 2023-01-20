from api.engine.document_interfaces import HTMLDocument, PDFDocument
from api.contract.edital.edital_templates import DTBB001, EditalRodapeDefault


#####################################################################################
# ------------------------------------- DTBB001 -------------------------------------#

class DTBB001Capa(DTBB001, HTMLDocument):

    document_name = "DTBB001 - CAPA"
    current_layer = "capa.html"


class DTBB001Miolo(DTBB001, PDFDocument):

    document_name = "DTBB001 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB001Rodape(EditalRodapeDefault):

    document_name = "DTBB001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB001 -------------------------------------#
#####################################################################################
