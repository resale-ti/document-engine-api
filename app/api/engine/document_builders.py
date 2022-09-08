from abc import abstractmethod
from api.engine.document_interfaces import HTMLDocumentInterface


class HTMLDocumentBuilder(HTMLDocumentInterface):

    document_content = None
    document_name = None

    def __init__(self, object_id, data=[]) -> None:
        # isso aqui é instanciado dentro de get_documents_objects_list no meu aqui tá vazio por enquanto
        self.object_id = object_id
        self.data = data

    @abstractmethod
    def build_html_layers():
        pass

    def build(self):
        html_layers_list = self.build_html_layers()
