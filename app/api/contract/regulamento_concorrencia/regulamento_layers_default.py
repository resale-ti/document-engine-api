from api.engine.document_interfaces import HTMLDocument
from api.contract.regulamento_concorrencia import PATH_REGULAMENTO_FOLDER


#####################################################################################
# ---------------------------------- DEFAULTS --------------------------------------#
class RegulamentoConcorrenciaRodapeTituloDefault(HTMLDocument):

    current_layer = "anexo-titulo.html"
    folder = "utils"
    template_path = PATH_REGULAMENTO_FOLDER


class RegulamentoConcorrenciaRodapeImovelDefault(HTMLDocument):

    folder = "utils"
    template_path = PATH_REGULAMENTO_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "anexo-imovel.html"
        self.data = imovel
# ---------------------------------- DEFAULTS --------------------------------------#
#####################################################################################


"""
Layers Default para modelo de regulamento MLPVA001 para venda amigável
"""
#####################################################################################
# ----------------------------- DEFAULTS MLPVA001 ----------------------------------#

class RegulamentoConcorrenciaRodapeImovelDefaultMLPVA001(HTMLDocument):

    folder = "MLPVA_001"
    template_path = PATH_REGULAMENTO_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "anexo-imovel.html"
        self.data = imovel
# ----------------------------- DEFAULTS MLPVA001 ----------------------------------#
#####################################################################################


"""
Layers para modelo de regulamento DOR027 para venda amigável
"""
#####################################################################################
# ------------------------------------- DOR027 -------------------------------------#

class RegulamentoConcorrenciaRodapeImovelDefaultDOR027(HTMLDocument):

    folder = "DOR_027"
    template_path = PATH_REGULAMENTO_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "anexo-imovel.html"
        self.data = imovel
