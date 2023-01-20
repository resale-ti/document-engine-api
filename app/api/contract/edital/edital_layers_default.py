from api.engine.document_interfaces import HTMLDocument
from api.contract.edital import PATH_EDITAL_FOLDER

class EditalRodapeImovelTituloDefault(HTMLDocument):

    folder = "DTBB001"
    template_path = PATH_EDITAL_FOLDER
    current_layer = "imovel-titulo.html"
class EditalRodapeImovelDefault(HTMLDocument):

    folder = "DTBB001"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel
