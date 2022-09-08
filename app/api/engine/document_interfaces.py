from abc import ABC, abstractmethod


class DocumentInterface(ABC):
    pass
    # @abstractmethod
    # def get_document_name(self):
    #     pass

    # @abstractmethod
    # def get_document_content(self):
    #     pass


class HTMLDocumentInterface(DocumentInterface):

    @abstractmethod
    def build(self):
        pass


class HTMLLayerInterface(ABC):

    LAYER_PATH = None

    @abstractmethod
    def get_layer_content(self):
        pass