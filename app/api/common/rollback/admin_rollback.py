from api.common.repositories.document_repository import DocumentRepository
from api.common.repositories.history_repository import HistoryRepository


class AdminRollback:
    def __init__(self, task_payload: dict) -> None:
        self.payload = task_payload.get("task_request")

    def document_handler(self) -> None:
        wallet_id = self.payload.get("id_obj")
        print(f"Inativando documentos p/ Carteira: {wallet_id}")

        regulamentos = DocumentRepository().get_wallet_regulamento(wallet_id=wallet_id)

        if regulamentos:
            docs = [regulamento.id for regulamento in regulamentos]

            print(f"{len(docs)} regulamentos serão inativados! ({docs})")

            DocumentRepository().inactive_many_documents(tuple(docs))
            HistoryRepository().insert_wallet_history(fields = {
                "documento_status": {"new": "inactive"},
                "description": "Documentos Inativos (Falha na geração do Regulamento)"}, wallet_id=wallet_id)
