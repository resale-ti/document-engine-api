from api.engine.document_interfaces import HTMLDocument, PDFDocument
from api.contract.edital.edital_templates import MLP002, RegulamentoConcorrenciaRodapeDefault


#####################################################################################
# ------------------------------------- DTBB001 -------------------------------------#

class DTBB001Capa(MLP002, HTMLDocument):

    document_name = "DTBB001 - CAPA"
    current_layer = "capa.html"


class DTBB001Miolo(MLP002, PDFDocument):

    document_name = "DTBB001 - MIOLO"
    current_layer = "miolo.pdf"


class DTBB001Rodape(RegulamentoConcorrenciaRodapeDefault):

    document_name = "DTBB001 - RODAPÉ"
    stylesheets = "edital.css"
    current_layer = []

# ------------------------------------- DTBB001 -------------------------------------#
#####################################################################################
