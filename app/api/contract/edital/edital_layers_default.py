from api.engine.document_interfaces import HTMLDocument
from api.contract.edital import PATH_EDITAL_FOLDER


class EditalRodapeDefault(HTMLDocument):

    current_layer = ""
    folder = ""
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.data = imovel
        
class EditalImovelDefault(HTMLDocument):

    folder = ""
    template_path = PATH_EDITAL_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "imovel.html"
        self.data = imovel
        
######################################################################################
# ------------------------------------- DTBB001 -------------------------------------#
class EditalDTBB001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTBB001"
class EditalDTBB001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTBB001"
# ------------------------------------- DTBB001 -------------------------------------#
######################################################################################

######################################################################################
# ------------------------------------- DTBB002 -------------------------------------#
class EditalDTBB002RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTBB002"
class EditalDTBB002RodapeImovelDefault(EditalImovelDefault):

    folder = "DTBB002"
# ------------------------------------- DTBB002 -------------------------------------#
######################################################################################

######################################################################################
# ------------------------------------- DTBB003 -------------------------------------#
class EditalDTBB003RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTBB003"
class EditalDTBB003RodapeImovelDefault(EditalImovelDefault):

    folder = "DTBB003"
# ------------------------------------- DTBB003 -------------------------------------#
######################################################################################
######################################################################################
# ------------------------------------- DTBB004 -------------------------------------#
class EditalDTBB004RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTBB004"
class EditalDTBB004RodapeImovelDefault(EditalImovelDefault):

    folder = "DTBB004"
# ------------------------------------- DTBB004 -------------------------------------#
######################################################################################
######################################################################################
# ------------------------------------- DTBB005 -------------------------------------#
class EditalDTBB005RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTBB005"
class EditalDTBB005RodapeImovelDefault(EditalImovelDefault):

    folder = "DTBB005"
# ------------------------------------- DTBB005 -------------------------------------#
######################################################################################
######################################################################################
# ------------------------------------- DTBB006 -------------------------------------#
class EditalDTBB006RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTBB006"
class EditalDTBB006RodapeImovelDefault(EditalImovelDefault):

    folder = "DTBB006"
# ------------------------------------- DTBB006 -------------------------------------#
######################################################################################
