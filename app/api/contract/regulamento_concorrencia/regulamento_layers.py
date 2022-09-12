
import os
from pathlib import Path
from api.engine.document_interfaces import HTMLDocument, PDFDocument


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
template_path = os.path.join(BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')


#####################################################################################
# ---------------------------------- DEFAULTS --------------------------------------#
class RegulamentoConcorrenciaRodapeTituloDefault(HTMLDocument):

    current_layer = "anexo-titulo.html"
    folder = "utils"
    template_path = template_path


class RegulamentoConcorrenciaRodapeImovelDefault(HTMLDocument):

    folder = "utils"
    template_path = template_path

    def __init__(self, imovel) -> None:
        self.current_layer = "anexo-imovel.html"
        self.data = imovel
# ---------------------------------- DEFAULTS --------------------------------------#
#####################################################################################


#####################################################################################
# ------------------------------------- MLP002 -------------------------------------#
from api.contract.regulamento_concorrencia.regulamento_templates import MLP002, RegulamentoConcorrenciaRodapeDefault

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
