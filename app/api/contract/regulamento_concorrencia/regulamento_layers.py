
import os
from pathlib import Path
from api.engine.document_interfaces import HTMLDocument, PDFDocument
from api.contract.regulamento_concorrencia.regulamento_templates import MLP002

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
template_path = os.path.join(BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')


class RegulamentoConcorrenciaBase:
    template_path = template_path

#####################################################################################
# ---------------------------------- DEFAULTS --------------------------------------#
class RegulamentoConcorrenciaRodapeDefault(RegulamentoConcorrenciaBase):

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def instance_layers(self) -> None:
        # current_layer vai rolando um append de cada layer que vai precisar.
        self.current_layer.append(RegulamentoConcorrenciaRodapeTituloDefault())

        for imovel in self.data.get('imoveis'):
            self.current_layer.append(
                RegulamentoConcorrenciaRodapeImovelDefault(imovel))
        
        return self.current_layer

    def build(self, engine):
        html = ""
        layers = self.instance_layers()

        for document in layers:
            html += engine._generate_html_with_data(document)

        default_style = os.path.join(self.template_path, self.stylesheets)

        return engine.generate_pdf_byte(html=html, default_style=default_style)


class RegulamentoConcorrenciaRodapeTituloDefault(RegulamentoConcorrenciaBase, HTMLDocument):

    current_layer = "anexo-titulo.html"
    folder = "utils"


class RegulamentoConcorrenciaRodapeImovelDefault(RegulamentoConcorrenciaBase, HTMLDocument):

    folder = "utils"

    def __init__(self, imovel) -> None:
        self.current_layer = "anexo-imovel.html"
        self.data = imovel
# ---------------------------------- DEFAULTS --------------------------------------#
#####################################################################################


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
