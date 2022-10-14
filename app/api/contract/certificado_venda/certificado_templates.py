import os
from api.contract.certificado_venda import PATH_CERTIFICADO_FOLDER
from api.contract.contract_builder_interface import ContractBuilderInterface
from api.contract.certificado_venda.certificado_layers_default import CertificadoVendaRodapeLogsDefault, CertificadoVendaRodapeTituloDefault

class CertificadoVendaRodapeDefault(ContractBuilderInterface):

    template_path = PATH_CERTIFICADO_FOLDER

    def __init__(self, property_id, data) -> None:
        self.property_id = property_id
        self.data = data

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(CertificadoVendaRodapeTituloDefault())

        # substituir imovel por propoerty_id?
        for imovel in self.data.get('imoveis'):
            current_layer.append(
                CertificadoVendaRodapeLogsDefault(imovel))

        return current_layer

    def build(self, engine):
        html = ""
        self.current_layer = self.instance_layers()

        for document in self.current_layer:
            html += engine._generate_html_with_data(document)

        default_style = os.path.join(self.template_path, self.stylesheets)

        return engine.generate_pdf_byte(html=html, default_style=default_style)

    
class CertificadoVenda(ContractBuilderInterface):

    folder = "Certificado_Venda"
    template_path = PATH_CERTIFICADO_FOLDER
    stylesheets = "certificado_venda.css"

    def __init__(self, property_id, data) -> None:
        self.property_id = property_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes