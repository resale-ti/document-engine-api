from api.engine.builder import BuilderEngine
from api.engine.document_builders import HTMLDocumentBuilder

class ContractBuilderBase:

    def __init__(self) -> None:
        self.engine = BuilderEngine(stylesheet_path=self._stylesheet_path, header_logo=self._header_logo)

    def get_file_stream(self):
        """esse file stream vai ser do builder Engine"""
        pass

    def _generate_documents(self, documents):
        self.__handle_with_html_docs(documents)
        self.__handle_with_pdfurl_docs(documents)

    def __handle_with_html_docs(self, documents):
        html_documents = list(filter(lambda document: isinstance(document, HTMLDocumentBuilder), documents))
        
        for document in html_documents:
            document.build()
            
        return ""

    def __handle_with_pdfurl_docs(self, documents):
        pass