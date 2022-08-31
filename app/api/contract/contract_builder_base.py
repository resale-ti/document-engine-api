from api.engine.builder import BuilderEngine

class ContractBuilderBase:

    def __init__(self) -> None:
        self.engine = BuilderEngine(stylesheet_path=self._stylesheet_path, header_logo=self._header_logo)

    def get_file_stream(self):
        """esse file stream vai ser do builder Engine"""
        pass

    def _generate_documents(self):
        pass

    def __handle_with_html_docs(self):
        pass

    def __handle_with_pdfurl_docs(self):
        pass