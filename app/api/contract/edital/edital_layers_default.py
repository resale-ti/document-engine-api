from api.engine.document_interfaces import HTMLDocument
from api.contract.edital import PATH_EDITAL_FOLDER


#####################################################################################
# ---------------------------------- DEFAULTS --------------------------------------#
class EditalRodapeTituloDefault(HTMLDocument):

    current_layer = "anexo-titulo.html"
    folder = "utils"
    template_path = PATH_EDITAL_FOLDER


class EditalRodapeImovelDefault(HTMLDocument):

    folder = "utils"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "anexo-imovel.html"
        self.data = imovel
# ---------------------------------- DEFAULTS --------------------------------------#
#####################################################################################