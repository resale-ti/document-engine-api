from api.engine.builder import BuilderEngine
from abc import abstractmethod
import base64


class ContractBuilderBase:

    def __init__(self) -> None:
        self.engine = BuilderEngine()

    def _generate_documents(self, documents):
        """
        Método responsável por chamar o build de um Documento e receber o PDF montado em forma de file bytes.
        Após isso adiciona ao Writer o file_bytes.
        """
        for document in documents:
            file_bytes = document.build(self.engine)

            if file_bytes is not None:
                self.engine._handle_file_bytes(file_bytes)
            else:
                raise Exception(f"Cannot generate file bytes. Document: {document.__class__.__name__}.")

        # Erase file = False - This will generate a file in your file tree. | TRUE by default.
        enconded_bytes = self.engine._get_file_bytes_pdf_writer()

        # RETURN FILE BYTES ENCONDED FROM FILE
        return base64.b64encode(enconded_bytes)

    @abstractmethod
    def build(self):
        pass
