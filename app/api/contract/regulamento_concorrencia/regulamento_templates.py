import os
from api.contract.regulamento_concorrencia import PATH_REGULAMENTO_FOLDER
from api.contract.contract_builder_interface import ContractBuilderInterface
from api.contract.regulamento_concorrencia.regulamento_layers_default import RegulamentoConcorrenciaRodapeTituloDefault, RegulamentoConcorrenciaRodapeImovelDefault, \
    RegulamentoConcorrenciaRodapeImovelDefaultMLPVA001, RegulamentoConcorrenciaRodapeImovelDefaultDOR027

#####################################################################################
# ------------------------------------- MLP002 -------------------------------------#
class RegulamentoConcorrenciaRodapeDefault(ContractBuilderInterface):

    template_path = PATH_REGULAMENTO_FOLDER

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(RegulamentoConcorrenciaRodapeTituloDefault())

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                RegulamentoConcorrenciaRodapeImovelDefault(imovel))

        return current_layer

    def build(self, engine):
        html = ""
        self.current_layer = self.instance_layers()

        for document in self.current_layer:
            html += engine._generate_html_with_data(document)

        default_style = os.path.join(self.template_path, self.stylesheets)

        return engine.generate_pdf_byte(html=html, default_style=default_style)


class MLP002(ContractBuilderInterface):

    folder = "MLP_002"
    template_path = PATH_REGULAMENTO_FOLDER
    stylesheets = "regulamento.css"

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes

# ------------------------------------- MLP002 -------------------------------------#
#####################################################################################


"""
Templates para modelo de regulamento MLPVA001 para venda amigável
"""
#####################################################################################
# ------------------------------------ MLPVA001 ------------------------------------#

class RegulamentoConcorrenciaRodapeDefaultMLPVA001(ContractBuilderInterface):

    template_path = PATH_REGULAMENTO_FOLDER

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(RegulamentoConcorrenciaRodapeTituloDefault())

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                RegulamentoConcorrenciaRodapeImovelDefaultMLPVA001(imovel))

        return current_layer

    def build(self, engine):
        html = ""
        self.current_layer = self.instance_layers()

        for document in self.current_layer:
            html += engine._generate_html_with_data(document)

        default_style = os.path.join(self.template_path, self.stylesheets)

        return engine.generate_pdf_byte(html=html, default_style=default_style)

class MLPVA001(ContractBuilderInterface):
    folder = "MLPVA_001"
    template_path = PATH_REGULAMENTO_FOLDER
    stylesheets = "regulamento.css"

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes

# ------------------------------------- MLPVA001 -----------------------------------#
#####################################################################################


# ------------------------------------- DOR027 -------------------------------------#

class RegulamentoConcorrenciaRodapeDefaultDOR027(ContractBuilderInterface):

    template_path = PATH_REGULAMENTO_FOLDER
    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def instance_layers(self) -> None:
        current_layer = []
        current_layer.append(RegulamentoConcorrenciaRodapeTituloDefault())
        for imovel in self.data.get('imoveis'):
            current_layer.append(
                RegulamentoConcorrenciaRodapeImovelDefaultDOR027(imovel))
        return current_layer

    def build(self, engine):
        html = ""
        self.current_layer = self.instance_layers()
        for document in self.current_layer:
            html += engine._generate_html_with_data(document)
        default_style = os.path.join(self.template_path, self.stylesheets)
        return engine.generate_pdf_byte(html=html, default_style=default_style)

class DOR027(ContractBuilderInterface):
    folder = "DOR_027"
    template_path = PATH_REGULAMENTO_FOLDER
    stylesheets = "regulamento.css"

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes
# ------------------------------------- DOR027 -------------------------------------#
#####################################################################################