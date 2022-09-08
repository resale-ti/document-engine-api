from api.engine.document_builders import HTMLDocumentBuilder
from api.contract.regulamento_concorrencia.regulamento_layers import MLP002CapaLayer

# MLP_002 ---------------------------------------------------
class MLP002Capa(HTMLDocumentBuilder):

    document_name = "MLP_002 - CAPA"

    def build_html_layers(self):
        data = self.data
        
        html_layers_list = [MLP002CapaLayer(data)]

        return data
# MLP_002 ---------------------------------------------------


class RegulamentoDocumentsFactory:

    MLP_002 = [MLP002Capa]

    def get_instance(self, wallet_id, data):
        regulamento_type = data.get("regulamento")
        
        if regulamento_type == "MLP_002":
            return [MLP002Capa(wallet_id, data)]

        return ""
