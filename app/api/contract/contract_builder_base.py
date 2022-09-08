from api.engine.builder import BuilderEngine


class ContractBuilderBase:

    def __init__(self) -> None:
        self.engine = BuilderEngine()

    def _generate_documents(self, documents):
        file_bytes = self.engine.build(documents)
        
        return file_bytes
