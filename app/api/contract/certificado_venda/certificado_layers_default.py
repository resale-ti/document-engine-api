from api.engine.document_interfaces import HTMLDocument
from api.contract.certificado_venda import PATH_CERTIFICADO_FOLDER


#####################################################################################
# ---------------------------------- DEFAULTS --------------------------------------#
class CertificadoVendaRodapeTituloDefault(HTMLDocument):

    current_layer = "logs-title.html"
    folder = "utils"
    template_path = PATH_CERTIFICADO_FOLDER


class CertificadoVendaRodapeLogsDefault(HTMLDocument):

    folder = "utils"
    template_path = PATH_CERTIFICADO_FOLDER

    def __init__(self, imovel) -> None:
        self.current_layer = "logs-body.html"
        self.data = imovel
# ---------------------------------- DEFAULTS --------------------------------------#
#####################################################################################