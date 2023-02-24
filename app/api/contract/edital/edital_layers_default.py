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
# ------------------------------------- EditalDT003_002 -------------------------------------#
class EditalDT003_002RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DT003_002"
class EditalDT003_002RodapeImovelDefault(EditalImovelDefault):

    folder = "DT003_002"
# ------------------------------------- EditalDT003_002 -------------------------------------#
######################################################################################
######################################################################################
# ------------------------------------- DTBNC001_001 -------------------------------------#
class EditalDTBNC001_001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTBNC001_001"
class EditalDTBNC001_001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTBNC001_001"
# ------------------------------------- DTBNC001_001 -------------------------------------#
############################################################################################################################################################################
# ------------------------------------- DTDV001_001 -------------------------------------#
class EditalDTDV001_001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTDV001_001"
class EditalDTDV001_001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTDV001_001"
# ------------------------------------- DTDV001_001 -------------------------------------#
############################################################################################################################################################################
# ------------------------------------- DTEM_001 -------------------------------------#
class EditalDTEM_001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTEM_001"
class EditalDTEM_001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTEM_001"
# ------------------------------------- DTEM_001 -------------------------------------#
############################################################################################################################################################################
# ------------------------------------- DTEMG001 -------------------------------------#
class EditalDTEMG001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTEMG001"
class EditalDTEMG001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTEMG001"
# ------------------------------------- DTEMG001 -------------------------------------#
############################################################################################################################################################################
# ------------------------------------- DTENF_NPL_001_004 -------------------------------------#
class EditalDTENF_NPL_001_004RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTENF_NPL_001_004"
class EditalDTENF_NPL_001_004RodapeImovelDefault(EditalImovelDefault):

    folder = "DTENF_NPL_001_004"
# ------------------------------------- DTENF_NPL_001_004 -------------------------------------#
############################################################################################################################################################################
# ------------------------------------- DTITPV001_001 -------------------------------------#
class EditalDTITPV001_001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTITPV001_001"
class EditalDTITPV001_001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTITPV001_001"
# ------------------------------------- DTITPV001_001 -------------------------------------#
######################################################################################
############################################################################################################################################################################
# ------------------------------------- DTPX001_001 -------------------------------------#
class EditalDTPX001_001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTPX001_001"
class EditalDTPX001_001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTPX001_001"
# ------------------------------------- DTPX001_001 -------------------------------------#
######################################################################################
# ------------------------------------- DTRD001_001 -------------------------------------#
class EditalDTRD001_001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTRD001_001"
class EditalDTRD001_001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTRD001_001"
# ------------------------------------- DTRD001_001 -------------------------------------#
######################################################################################
# ------------------------------------- DTTRI001_001 -------------------------------------#
class EditalDTTRI001_001RodapeTituloDefault(EditalRodapeDefault):

    current_layer = "imovel-titulo.html"
    folder = "DTTRI001_001"
class EditalDTTRI001_001RodapeImovelDefault(EditalImovelDefault):

    folder = "DTTRI001_001"
# ------------------------------------- DTTRI001_001 -------------------------------------#
######################################################################################