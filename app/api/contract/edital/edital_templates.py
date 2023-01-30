import os
from api.contract.edital import PATH_EDITAL_FOLDER
from api.contract.contract_builder_interface import ContractBuilderInterface
import api.contract.edital.edital_layers_default as ly


class EditalDTBB001RodapeDefault(ContractBuilderInterface):

    template_path = PATH_EDITAL_FOLDER

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB001RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB001RodapeImovelDefault(imovel))

        return current_layer

    def build(self, engine):
        html = ""
        self.current_layer = self.instance_layers()

        for document in self.current_layer:
            html += engine._generate_html_with_data(document)

        default_style = os.path.join(self.template_path, self.stylesheets)

        return engine.generate_pdf_byte(html=html, default_style=default_style)

class EditalDTBB002RodapeDefault(EditalDTBB001RodapeDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB002RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB002RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB003RodapeDefault(EditalDTBB001RodapeDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB003RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB003RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB004RodapeDefault(EditalDTBB001RodapeDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB004RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB004RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB005RodapeDefault(EditalDTBB001RodapeDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB005RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB005RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB006RodapeDefault(EditalDTBB001RodapeDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB006RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB006RodapeImovelDefault(imovel))

        return current_layer


class DTBB001(ContractBuilderInterface):

    folder = "DTBB001"
    template_path = PATH_EDITAL_FOLDER
    stylesheets = "edital.css"

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes


class DTBB002(DTBB001):
    folder = "DTBB002"


class DTBB003(DTBB001):
    folder = "DTBB003"


class DTBB004(DTBB001):
    folder = "DTBB004"


class DTBB005(DTBB001):
    folder = "DTBB005"


class DTBB006(DTBB001):
    folder = "DTBB006"


