from api.engine.document_interfaces import HTMLDocument, PDFDocument
from api.contract.regulamento_concorrencia.regulamento_templates import MLP002


class MLP002Capa(MLP002, HTMLDocument):

    document_name = "MLP_002 - CAPA"
    current_layer = "capa.html"


class MLP002Miolo(MLP002, PDFDocument):

    document_name = "MLP_002 - MIOLO"
    current_layer = "miolo.pdf"


class RegulamentoDocumentsFactory:

    def get_instance(self, wallet_id, data):
        regulamento_type = data.get("regulamento")

        if regulamento_type == "MLP_002":
            return [MLP002Capa(wallet_id, data), MLP002Miolo(wallet_id, data)]

        return ""
