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