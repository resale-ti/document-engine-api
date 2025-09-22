from api.engine.document_interfaces import HTMLDocument, PDFDocument
from api.contract.regulamento_concorrencia.regulamento_templates import MLP002, RegulamentoConcorrenciaRodapeDefault, MLPVA001, RegulamentoConcorrenciaRodapeDefaultMLPVA001, DOR027, RegulamentoConcorrenciaRodapeDefaultDOR027


#####################################################################################
# ------------------------------------- MLP002 -------------------------------------#

class MLP002Capa(MLP002, HTMLDocument):

    document_name = "MLP_002 - CAPA"
    current_layer = "capa.html"


class MLP002Miolo(MLP002, PDFDocument):

    document_name = "MLP_002 - MIOLO"
    current_layer = "miolo.pdf"


class MLP002Rodape(RegulamentoConcorrenciaRodapeDefault):

    document_name = "MLP_002 - RODAPÉ"
    stylesheets = "regulamento.css"
    current_layer = []

# ------------------------------------- MLP002 -------------------------------------#
#####################################################################################



"""
Layers para modelo de regulamento MLPVA001 para venda amigável
"""
#####################################################################################
# ----------------------------------- MLPVA001 -------------------------------------#

class MLPVA001Capa(MLPVA001, HTMLDocument):

    document_name = "MLPVA_001 - CAPA"
    current_layer = "capa.html"


class MLPVA001Miolo(MLPVA001, PDFDocument):

    document_name = "MLPVA_001 - MIOLO"
    current_layer = "miolo.pdf"


class MLPVA001Rodape(RegulamentoConcorrenciaRodapeDefaultMLPVA001):

    document_name = "MLPVA_001 - RODAPÉ"
    stylesheets = "regulamento.css"
    current_layer = []

# ------------------------------------- MLPVA001 -----------------------------------#
#####################################################################################


"""
Layers para modelo de regulamento DOR027 para venda amigável
"""
class DOR027Capa(DOR027, HTMLDocument):

    document_name = "DOR_027 - CAPA"
    current_layer = "capa.html"


class DOR027Miolo(DOR027, PDFDocument):

    document_name = "DOR_027 - MIOLO"
    current_layer = "miolo.pdf"


class DOR027Rodape(RegulamentoConcorrenciaRodapeDefaultDOR027):

    document_name = "DOR_027 - RODAPÉ"
    stylesheets = "regulamento.css"
    current_layer = []

# ------------------------------------- DOR027 -------------------------------------#
#####################################################################################
