from api.engine.document_interfaces import HTMLDocument
from api.contract.edital import PATH_EDITAL_FOLDER


class EditalDTBB001RodapeTituloDefault(HTMLDocument):

    current_layer = "imovel-titulo.html"
    folder = "DTBB001"
    template_path = PATH_EDITAL_FOLDER


class EditalDTBB001RodapeImovelDefault(HTMLDocument):

    folder = "DTBB001"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel
        
class EditalDTBB002RodapeTituloDefault(HTMLDocument):

    current_layer = "imovel-titulo.html"
    folder = "DTBB002"
    template_path = PATH_EDITAL_FOLDER


class EditalDTBB002RodapeImovelDefault(HTMLDocument):

    folder = "DTBB002"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel
        
class EditalDTBB003RodapeTituloDefault(HTMLDocument):

    current_layer = "imovel-titulo.html"
    folder = "DTBB003"
    template_path = PATH_EDITAL_FOLDER


class EditalDTBB003RodapeImovelDefault(HTMLDocument):

    folder = "DTBB003"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel


class EditalDTBB004RodapeTituloDefault(HTMLDocument):

    current_layer = "imovel-titulo.html"
    folder = "DTBB004"
    template_path = PATH_EDITAL_FOLDER


class EditalDTBB004RodapeImovelDefault(HTMLDocument):

    folder = "DTBB004"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel


class EditalDTBB005RodapeTituloDefault(HTMLDocument):

    current_layer = "imovel-titulo.html"
    folder = "DTBB005"
    template_path = PATH_EDITAL_FOLDER


class EditalDTBB005RodapeImovelDefault(HTMLDocument):

    folder = "DTBB005"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel


class EditalDTBB006RodapeTituloDefault(HTMLDocument):

    current_layer = "imovel-titulo.html"
    folder = "DTBB006"
    template_path = PATH_EDITAL_FOLDER


class EditalDTBB006RodapeImovelDefault(HTMLDocument):

    folder = "DTBB006"
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel

