import os
from api.contract.edital import PATH_EDITAL_FOLDER
from api.contract.contract_builder_interface import ContractBuilderInterface
import api.contract.edital.edital_layers_default as ly

class EditalDefault(ContractBuilderInterface):

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

class EditalDTBB001RodapeDefault(EditalDefault):

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

class EditalDTBB002RodapeDefault(EditalDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB002RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB002RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB003RodapeDefault(EditalDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB003RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB003RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB004RodapeDefault(EditalDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB004RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB004RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB005RodapeDefault(EditalDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB005RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB005RodapeImovelDefault(imovel))

        return current_layer

class EditalDTBB006RodapeDefault(EditalDefault):

    def instance_layers(self) -> None:
        current_layer = []

        current_layer.append(ly.EditalDTBB006RodapeTituloDefault(self.data))

        for imovel in self.data.get('imoveis'):
            current_layer.append(
                ly.EditalDTBB006RodapeImovelDefault(imovel))

        return current_layer


class TemplateDefault(ContractBuilderInterface):

    template_path = PATH_EDITAL_FOLDER
    stylesheets = "edital.css"

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes

class DTBB001(TemplateDefault):

    folder = "DTBB001"


class DTBB002(TemplateDefault):
    folder = "DTBB002"


class DTBB003(TemplateDefault):
    folder = "DTBB003"


class DTBB004(TemplateDefault):
    folder = "DTBB004"


class DTBB005(TemplateDefault):
    folder = "DTBB005"


class DTBB006(TemplateDefault):
    folder = "DTBB006"


class DT003_002(TemplateDefault):
    folder = "DT003_002"
    
class DTBNC001_001(TemplateDefault):
    folder = "DTBNC001_001"


class DTDV001_001(TemplateDefault):
    folder = "DTDV001_001"


class DTEM_001(TemplateDefault):
    folder = "DTEM_001"


class DTEMG001(TemplateDefault):
    folder = "DTEMG001"


