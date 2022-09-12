import os
from pathlib import Path
from app.api.contract.contract_builder_interface import ContractBuilderInterface
from api.contract.regulamento_concorrencia.regulamento_layers import RegulamentoConcorrenciaRodapeTituloDefault, RegulamentoConcorrenciaRodapeImovelDefault


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
template_path = os.path.join(BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')


class RegulamentoConcorrenciaRodapeDefault(ContractBuilderInterface):

    template_path = template_path

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def instance_layers(self) -> None:
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


class MLP002(ContractBuilderInterface):

    folder = "MLP_002"
    template_path = template_path
    stylesheets = "regulamento.css"

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes
